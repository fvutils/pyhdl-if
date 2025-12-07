#!/bin/sh

script_dir=$(dirname $(realpath $0))
proj_dir=$(cd ${script_dir}/../../../.. ; pwd)
export PYTHONPATH=${proj_dir}/python:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs()))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

python3 -m hdl_if api-gen-sv -m sv2py2sv_call -o MyC.svh
if test $? -ne 0; then exit 1; fi

flags=""

for lib in $libs; do
    lib=`echo $lib | sed -e 's/\.so//g'`
    flags="$flags -sv_lib $lib"
done

echo "flags: ${flags}"

vlib work
vlog -sv \
	+incdir+${share}/dpi \
	${share}/dpi/pyhdl_if.sv \
	sv2py2sv_call.sv 
if test $? -ne 0; then exit 1; fi

vsim -c -do "run -a; quit -f" sv2py2sv_call ${flags}
if test $? -ne 0; then exit 1; fi


