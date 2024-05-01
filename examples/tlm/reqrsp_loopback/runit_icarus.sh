#!/bin/sh

script_dir=$(dirname $(realpath $0))
proj_dir=$(cd ../../.. ; pwd)
export PYTHONPATH=${proj_dir}/src:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs("vpi")))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

python3 -m hdl_if ifc-gen-sv -m reqrsp_loopback ReqRspLoopback -o ReqRspLoopback.sv
if test $? -ne 0; then exit 1; fi

vvp_args=""
for l in $libs; do
    vvp_args="$vvp_args -m $l"
done

echo "share_call: '${share_call}'"

iverilog \
	${share}/pyhdl_if_req_fifo.sv \
	${share}/pyhdl_if_rsp_fifo.sv \
	${share}/pyhdl_if_reqrsp_fifo.sv \
	ReqRspLoopback.sv \
	reqrsp_loopback.sv -s reqrsp_loopback -o reqrsp_loopback.vvp
if test $? -ne 0; then exit 1; fi

#gdb --args vvp ${vvp_args} req_rsp_loopback.vvp
valgrind --tool=memcheck vvp ${vvp_args} reqrsp_loopback.vvp


