#!/bin/bash

script_dir=$(dirname $(realpath $0))
proj_dir=$(cd ${script_dir}/../../ ; pwd)

export PYTHONPATH=${proj_dir}/src:${PYTHONPATH}

vivado_bindir=$(dirname $(which xvlog))
uvm_home=$(cd ${vivado_bindir}/../data/xsim/system_verilog/uvm ; pwd)

xvlog --sv --lib uvm \
	-i ${proj_dir}/src/hdl_if/share/dpi \
	-i ${proj_dir}/src/hdl_if/share/uvm \
	${proj_dir}/src/hdl_if/share/dpi/pyhdl_if.sv \
	${proj_dir}/src/hdl_if/share/uvm/pyuvm_if.sv \
	top_pkg.sv top.sv
if test $? -ne 0; then exit 1; fi

xelab --snap top:snap top

xsim top:snap --testplusarg UVM_TESTNAME=base_test --runall

