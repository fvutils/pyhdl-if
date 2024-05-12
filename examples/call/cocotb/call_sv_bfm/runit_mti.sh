#!/bin/bash

example_dir=$(dirname $(realpath $0))
proj_dir=$(cd ${example_dir}/../../../.. ; pwd)
rundir=`pwd`

interp_bindir=${proj_dir}/packages/python/bin
interp=$interp_bindir/python
#export PYTHONPATH=${proj_dir}/src:${example_dir}:${PYTHONPATH}
export PYTHONPATH=${proj_dir}/src:${example_dir}

#interp_bindir=$rundir/example_venv/bin
#if test ! -d $rundir/example_venv; then
#    echo "Creating Python virtual environment"
#    python3 -m venv $rundir/example_venv
#    $interp -m pip install --upgrade pip
#    $interp -m pip install -r $example_dir/requirements.txt
#fi

cocotb_libdir=$(${interp_bindir}/cocotb-config --lib-dir)
libpython=$(${interp_bindir}/cocotb-config --libpython)

hdl_if_libs=$(${interp} -c "import hdl_if ; print(' '.join(hdl_if.libs('vpi')))")
hdl_if_share=$(${interp} -c "import hdl_if ; print(hdl_if.share())")

echo "hdl_if_libs=${hdl_if_libs}"
echo "libpython=${libpython}"

vsim_args=""
for lib in ${hdl_if_libs}; do
    lib=$(echo $lib | sed -e 's/\.so//')
    vsim_args="$vsim_args -sv_lib ${lib}"
done

# Generate the Wrapper API
 ${interp} -m hdl_if api-gen-sv -m call_sv_bfm
if test $? -ne 0; then exit 1; fi

vlib work
vlog -sv \
    +incdir+${hdl_if_share}/dpi \
    ${hdl_if_share}/dpi/pyhdl_if.sv \
    ${example_dir}/call_sv_bfm.sv 
if test $? -ne 0; then exit 1; fi

export PATH=${interp_bindir}:${PATH}
export LD_LIBRARY_PATH=$(dirname ${libpython}):${LD_LIBRARY_PATH}
export MODULE=call_sv_bfm

echo "PYTHON: `which python3`"

#valgrind="-valgrind --tool=memcheck"

vsim -c -do "run -a; quit -f" call_sv_bfm -dpioutoftheblue 1 \
	${valgrind} \
	-pli ${cocotb_libdir}/libcocotbvpi_modelsim.so \
    ${vsim_args}
#vsim -c -do "run -a; quit -f" call_sv_bfm \
#	-valgrind --tool=memcheck \
#    ${vsim_args}



