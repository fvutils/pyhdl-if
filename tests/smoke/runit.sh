#!/bin/sh

script_dir=$(dirname $(realpath $0))

verilator --binary -sv \
	+incdir+../../src/hdl_call_if/share/sv/ \
	../../src/hdl_call_if/share/sv/pyhdl_call_if.sv \
	top.sv \
	-LDFLAGS "-Wl,-L,/project/tools/python/3.12.0/lib -Wl,-rpath,/project/tools/python/3.12.0/lib -Wl,-lpython3.12 -rdynamic"

#GDB="gdb --args"
export LD_PRELOAD=/project/tools/python/3.12.0/lib/libpython3.12.so
#PYTHONPATH=${script_dir}/../../python ${GDB} ./obj_dir/Vpyhdl_call_if
PYTHONPATH=${script_dir}:${script_dir}/../../python ${GDB} ./obj_dir/Vpyhdl_call_if

