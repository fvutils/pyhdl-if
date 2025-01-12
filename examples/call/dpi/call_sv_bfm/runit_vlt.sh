#!/bin/bash

example_dir=$(dirname $(realpath $0))
rundir=`pwd`

interp_bindir=$rundir/example_venv/bin
interp=$interp_bindir/python
if test ! -d $rundir/example_venv; then
    echo "Creating Python virtual environment"
    python3 -m venv $rundir/example_venv
    $interp -m pip install --upgrade pip
    $interp -m pip install -r $example_dir/requirements.txt
fi

#cocotb_libdir=$(${interp_bindir}/cocotb-config --lib-dir)
#libpython=$(${interp_bindir}/cocotb-config --libpython)

hdl_if_libs=$(${interp} -c "import hdl_if ; print(' '.join(hdl_if.libs()))")
hdl_if_share=$(${interp} -c "import hdl_if ; print(hdl_if.share())")

echo "hdl_if_libs=${hdl_if_libs}"

vlt_args=""
for lib in ${hdl_if_libs}; do
#    dir=$(dirname $lib)
#    lib=$(echo $(basename $lib) | sed -e 's/\.so//' -e 's/^lib//g')
    vlt_args="$vlt_args -LDFLAGS $lib"
done

# Generate the Wrapper API
PYTHONPATH=$(pwd):${PYTHONPATH} ${interp} -m hdl_if api-gen-sv -m call_sv_bfm \
  -p call_sv_bfm_pkg -o call_sv_bfm_pkg.sv
if test $? -ne 0; then exit 1; fi

echo "[RUN CMD] verilator --binary -Wno-fatal -LDFLAGS -export-dynamic \
    +incdir+${hdl_if_share}/dpi \
    ${hdl_if_share}/dpi/pyhdl_if.sv \
    $example_dir/call_sv_bfm.sv ${vlt_args}"

verilator --binary -Wno-fatal -LDFLAGS -export-dynamic \
    +incdir+${hdl_if_share}/dpi \
    ${hdl_if_share}/dpi/pyhdl_if.sv \
    ${example_dir}/call_sv_bfm_pkg.sv \
    ${example_dir}/wb_init_bfm.sv \
    ${example_dir}/call_sv_bfm.sv ${vlt_args}
if test $? -ne 0; then exit 1; fi

export PATH=${interp_bindir}:${PATH}
export PYTHONPATH=$example_dir:${PYTHONPATH}
export LD_LIBRARY_PATH=$(dirname ${libpython}):${LD_LIBRARY_PATH}
export MODULE=call_sv_bfm

./obj_dir/Vpyhdl_if
