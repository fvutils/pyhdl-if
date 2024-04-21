#!/bin/sh

script_dir=$(dirname $(realpath $0))
proj_dir=$(cd ../../.. ; pwd)
export PYTHONPATH=${proj_dir}/python:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs()))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

python3 -m hdl_if ifc-gen-sv -m req_rsp_loopback ReqRspLoopback -o ReqRspLoopback.sv
if test $? -ne 0; then exit 1; fi

echo "share_call: '${share_call}'"

vsim_args=""
for lib in $libs; do
	lib=`echo $lib | sed -e 's/\.so//g'`
	vsim_args="$vsim_args -sv_lib $lib"
done

vlib work
vlog -sv \
	+incdir+${share}/dpi \
	${share}/dpi/pyhdl_if.sv \
	${share}/dpi/tlm_hdl2hvl_fifo.sv \
	${share}/dpi/tlm_hvl2hdl_fifo.sv \
	ReqRspLoopback.sv \
	req_rsp_loopback.sv 
time vsim -c -do "run -a; quit -f" req_rsp_loopback ${vsim_args}
if test $? -ne 0; then exit 1; fi


