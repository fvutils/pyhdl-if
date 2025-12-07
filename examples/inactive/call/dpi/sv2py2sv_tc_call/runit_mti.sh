#!/bin/sh

script_dir=$(dirname $(realpath $0))
proj_dir=$(cd ../../../.. ; pwd)
export PYTHONPATH=${proj_dir}/python:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs()))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

echo "libs: ${libs}"

vsim_args=""
for lib in $libs; do
	lib=`echo $lib | sed -e 's/\.so//g'`
	vsim_args="$vsim_args -sv_lib $lib"
done

python3 -m hdl_if api-gen-sv -m sv2py2sv_tc_call -o MyC.svh
if test $? -ne 0; then exit 1; fi

echo "share_call: '${share_call}'"

vlib work
vlog -sv \
	+incdir+${share}/dpi \
	${share}/dpi/pyhdl_if.sv \
	sv2py2sv_tc_call.sv
if test $? -ne 0; then exit 1; fi

time vsim -c -do "run -a; quit -f" sv2py2sv_tc_call ${vsim_args}
if test $? -ne 0; then exit 1; fi


