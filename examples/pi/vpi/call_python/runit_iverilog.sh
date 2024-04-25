#!/bin/bash -x

script_dir=$(dirname $(realpath $0))
pyhdl_if_dir=$(cd $script_dir/../../../.. ; pwd)

export PYTHONPATH=$pyhdl_if_dir/python:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs("vpi")))')

vvp_args=""
for l in $libs; do
    vvp_args="$vvp_args -m $l"
done

echo "libs: ${libs}"

iverilog -g2005-sv call_python.sv -s call_python -o call_python
if test $? -ne 0; then exit 1; fi

valgrind --tool=memcheck vvp $vvp_args call_python

