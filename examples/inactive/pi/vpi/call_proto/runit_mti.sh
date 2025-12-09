#!/bin/bash -x

script_dir=$(dirname $(realpath $0))
pyhdl_if_dir=$(cd $script_dir/../../../.. ; pwd)

export PYTHONPATH=$pyhdl_if_dir/python:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs("vpi")))')

vsim_args=""
for l in $libs; do
    vsim_args="$vsim_args -pli $l"
done

echo "vsim_args: ${vsim_args}"

vlib work
vlog -sv call_proto.sv
if test $? -ne 0; then exit 1; fi

vsim -batch -do "run -a; quit -f" $vsim_args call_proto 
if test $? -ne 0; then exit 1; fi


