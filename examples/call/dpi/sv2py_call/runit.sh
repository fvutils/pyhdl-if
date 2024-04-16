#!/bin/sh

script_dir=$(dirname $(realpath $0))
proj_dir=$(cd ${script_dir}/../../../../ ; pwd)
export PYTHONPATH=${proj_dir}/python:${script_dir}:${PYTHONPATH}

echo "PYTHONPATH=${PYTHONPATH}"

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs()))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

python3 -m hdl_if api-gen-sv -m sv2py_call -o MyC.svh
if test $? -ne 0; then exit 1; fi

echo "share: '${share}'"

verilator --binary \
	+incdir+${share}/dpi \
	${share}/dpi/pyhdl_if.sv \
	sv2py_call.sv -top sv2py_call \
	${libs} -LDFLAGS -Wl,--export-dynamic -LDFLAGS -Wl,-rpath,${python_libdir}
if test $? -ne 0; then exit 1; fi

./obj_dir/Vsv2py_call

