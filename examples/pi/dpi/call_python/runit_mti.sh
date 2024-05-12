#!/bin/bash

script_dir=$(dirname $(realpath $0))
pyhdl_if_dir=$(cd $script_dir/../../../.. ; pwd)

export PYTHONPATH=$pyhdl_if_dir/src:${script_dir}:${PYTHONPATH}

share=$(python3 -c 'import hdl_if; print(hdl_if.share())')
libs=$(python3 -c 'import hdl_if; print(" ".join(hdl_if.libs("vpi")))')

echo "libs: ${libs}"

vsim_args=""
for lib in ${libs}; do
    lib=$(echo $lib | sed -e 's/.so//g')
    vsim_args="$vsim_args -sv_lib ${lib}"
done

vlib work
vlog -sv \
	+incdir+${share}/dpi \
	${share}/dpi/pyhdl_if.sv \
	call_python.sv 
if test $? -ne 0; then exit 1; fi

vsim -c -do "run -a; quit -f" call_python ${vsim_args}
if test $? -ne 0; then exit 1; fi


