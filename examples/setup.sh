#!/bin/bash

set -e

examples_dir=$(dirname $(realpath $0))

# Parse arguments
pyhdl_wheel=""
tools_dir=""
dev_pkgs=false

print_help() {
  echo "Usage: $0 [options] [tools_dir]"
  echo ""
  echo "Arguments:"
  echo "  tools_dir                Directory in which to create tools (default: \$PWD/hdl_if_tools)"
  echo ""
  echo "Options:"
  echo "  -d, --dev-pkgs           Install dv-flow-mgr, dv-flow-libhdlsim, and pyhdl-if from development sources"
  echo "  -w, --pyhdl-wheel PATH   Path to a Python wheel to install for pyhdl-if instead of the PyPi version"
  echo "  -h, --help, -?, -help    Print this help message"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--dev-pkgs)
      dev_pkgs=true
      shift
      ;;
    -w|--pyhdl-wheel)
      pyhdl_wheel="$2"
      shift 2
      ;;
    -h|--help|-\?|-help)
      print_help
      ;;
    -*)
      echo "Error: Unknown option $1"
      print_help
      ;;
    *)
      if [[ -z "$tools_dir" ]]; then
        tools_dir="$1"
      else
        echo "Error: Unexpected argument $1"
        print_help
      fi
      shift
      ;;
  esac
done

# Create an installation in $tools_dir
if [[ -z "$tools_dir" ]]; then
  tools_dir=$(pwd)/hdl_if_tools
fi

echo "Note: installing to ${tools_dir}"

if test -d ${tools_dir}; then
  echo "Note: already exists. Exiting"
  exit 0
fi

mkdir -p ${tools_dir}/bin
mkdir -p ${tools_dir}/etc

# Fetch 'uv' for virtual environment creation
echo "Note: installing 'uv'"
curl -LsSf https://astral.sh/uv/install.sh -o ${tools_dir}/etc/inst_uv.sh

UV_INSTALL_DIR=${tools_dir}/bin /bin/bash ${tools_dir}/etc/inst_uv.sh

echo "Note: Setting up a virtual environment"

# Use the 'uv' just installed to setup a virtual environment with Python 3.12
${tools_dir}/bin/uv venv --python 3.12 ${tools_dir}/venv

# Install dv-flow packages from development sources if requested
if [[ "$dev_pkgs" == "true" ]]; then
  echo "Note: Installing dv-flow-mgr and dv-flow-libhdlsim from development sources"
  ${tools_dir}/bin/uv pip install --python ${tools_dir}/venv/bin/python \
    "dv-flow-mgr @ git+https://github.com/dv-flow/dv-flow-mgr" \
    "dv-flow-libhdlsim @ git+https://github.com/dv-flow/dv-flow-libhdlsim"
  pkgs="cocotb"
else
  pkgs="dv-flow-mgr dv-flow-libhdlsim cocotb"
fi

# Install packages using uv pip
if [[ -n "$pyhdl_wheel" ]]; then
  ${tools_dir}/bin/uv pip install --python ${tools_dir}/venv/bin/python $pkgs "$pyhdl_wheel"
elif [[ "$dev_pkgs" == "true" ]]; then
  # Install pyhdl-if from the parent directory (this repository)
  pyhdl_if_dir=$(dirname "$examples_dir")
  echo "Note: Installing pyhdl-if from development source: $pyhdl_if_dir"
  ${tools_dir}/bin/uv pip install --python ${tools_dir}/venv/bin/python $pkgs "$pyhdl_if_dir"
else
  ${tools_dir}/bin/uv pip install --python ${tools_dir}/venv/bin/python $pkgs pyhdl-if
fi

echo "Note: installing 'verilator'"

# Determine the system's OS
os_type=$(uname -s)
if [[ "$os_type" != "Linux" ]]; then
  echo "Error: This script only supports Linux. Detected OS: $os_type"
  exit 1
fi

# Get glibc version
glibc_version=$(ldd --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+$')
glibc_major=$(echo "$glibc_version" | cut -d. -f1)
glibc_minor=$(echo "$glibc_version" | cut -d. -f2)

echo "Note: Detected glibc version: $glibc_version"

# Download jq if not available
if ! command -v jq &> /dev/null; then
  echo "Note: jq not found, downloading..."
  curl -LsSf https://github.com/jqlang/jq/releases/download/jq-1.8.1/jq-linux-amd64 -o ${tools_dir}/bin/jq
  chmod +x ${tools_dir}/bin/jq
  jq_cmd="${tools_dir}/bin/jq"
else
  jq_cmd="jq"
fi

# Find the latest non-prerelease version of verilator-bin
echo "Note: Finding latest verilator-bin release..."
release_info=$(curl -sL "https://api.github.com/repos/EDAPack/verilator-bin/releases" | \
  $jq_cmd -r '[.[] | select(.prerelease == false)][0]')

tag_name=$(echo "$release_info" | $jq_cmd -r '.tag_name')
echo "Note: Latest verilator-bin release: $tag_name"

# Find the best matching glibc version asset
# Available: manylinux2014 (< 2.28), manylinux_2_28, manylinux_2_34
assets=$(echo "$release_info" | $jq_cmd -r '.assets[].name')

best_asset=""
best_glibc_minor=0

for asset in $assets; do
  if [[ "$asset" == *"manylinux_2_"*"_x86_64"* ]]; then
    # Extract glibc minor version (e.g., manylinux_2_34 -> 34)
    asset_glibc_minor=$(echo "$asset" | grep -oE 'manylinux_2_([0-9]+)' | grep -oE '[0-9]+$')
    if [[ -n "$asset_glibc_minor" ]]; then
      # Check if this glibc version is <= current and > best found so far
      if [[ "$glibc_major" -eq 2 && "$asset_glibc_minor" -le "$glibc_minor" && "$asset_glibc_minor" -gt "$best_glibc_minor" ]]; then
        best_asset="$asset"
        best_glibc_minor="$asset_glibc_minor"
      fi
    fi
  fi
done

# If no matching manylinux_2_XX found, try manylinux2014 as fallback
if [[ -z "$best_asset" ]]; then
  for asset in $assets; do
    if [[ "$asset" == *"manylinux2014_x86_64"* ]]; then
      best_asset="$asset"
      break
    fi
  done
fi

if [[ -z "$best_asset" ]]; then
  echo "Error: Could not find a compatible verilator-bin release for glibc $glibc_version"
  exit 1
fi

echo "Note: Selected verilator asset: $best_asset"

# Download and extract verilator
download_url=$(echo "$release_info" | $jq_cmd -r --arg asset "$best_asset" '.assets[] | select(.name == $asset) | .browser_download_url')

echo "Note: Downloading verilator from $download_url"
tmp_dir=$(mktemp -d)
curl -LsSf "$download_url" -o "${tmp_dir}/verilator.tar.gz"

echo "Note: Extracting verilator..."
tar -xzf "${tmp_dir}/verilator.tar.gz" -C ${tools_dir}
rm -rf "${tmp_dir}"

echo "Note: Adding setup script"

# Create setup.sh script
cat > ${tools_dir}/setup.sh << EOF
#!/bin/bash
export PATH="${tools_dir}/verilator/bin:${tools_dir}/bin:\${PATH}"
source ${tools_dir}/venv/bin/activate
EOF

# Create setup.csh script
cat > ${tools_dir}/setup.csh << EOF
#!/bin/csh
setenv PATH "${tools_dir}/verilator/bin:${tools_dir}/bin:\${PATH}"
source ${tools_dir}/venv/bin/activate.csh
EOF

echo "Note: done. Source ${tools_dir}/setup.[c]sh to configure the PATH"
