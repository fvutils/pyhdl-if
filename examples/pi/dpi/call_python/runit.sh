#!/bin/bash

script_dir=$(dirname $(realpath $0))
pyhdl_if_dir=$(cd $script_dir/../../../.. ; pwd)

export PYTHONPATH=$pyhdl_if_dir/python:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs()))')

echo "libs: ${libs}"

verilator --binary \
	+incdir+${share}/dpi \
	${share}/dpi/pyhdl_if.sv \
	call_python.sv \
	-top call_python ${libs} -LDFLAGS -Wl,--export-dynamic
if test $? -ne 0; then exit 1; fi

./obj_dir/Vcall_python

