#!/bin/sh

script_dir=$(dirname $(realpath $0))

vlib work
vlog -sv \
	+incdir+../../src/hdl_call_if/share/sv/ \
	../../src/hdl_call_if/share/sv/pyhdl_call_if.sv \
	top.sv

export LD_LIBRARY_PATH=/project/tools/python/3.12.0/lib 
export PYTHONPATH=${script_dir}:${script_dir}/../../python
export LD_PRELOAD=/project/tools/python/3.12.0/lib/libpython3.12.so

vsim -trace_dpi 1 -c -do "run -a; quit -f" top \
	-sv_lib /project/tools/python/3.12.0/lib/libpython3.12

#GDB="gdb --args"
#PYTHONPATH=${script_dir}:${script_dir}/../../python ${GDB} ./obj_dir/Vpyhdl_call_if
#PYTHONPATH=${script_dir}/../../python ${GDB} ./obj_dir/Vpyhdl_call_if

