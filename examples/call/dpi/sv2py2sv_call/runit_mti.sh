#!/bin/sh

export PYTHONPATH=`pwd`/../../../src:.:${PYTHONPATH}

share_pi=$(python3 -c 'import hdl_pi_if; print(hdl_pi_if.share())')
share_call=$(python3 -c 'import hdl_call_if; print(hdl_call_if.share())')
libs=$(python3 -c 'import hdl_pi_if; print(" ".join(hdl_pi_if.libs()))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

python3 -m hdl_call_if gen-sv -m sv2py2sv_call -o MyC.svh
if test $? -ne 0; then exit 1; fi

flags=""

for lib in $libs; do
    lib=`echo $lib | sed -e 's/\.so//g'`
    flags="$flags -sv_lib $lib"
done

echo "flags: ${flags}"

vlib work
vlog -sv \
	+incdir+${share_pi}/dpi \
	+incdir+${share_call}/dpi \
	${share_pi}/dpi/pyhdl_dpi_if.sv \
	${share_call}/sv/pyhdl_call_if.sv \
	sv2py2sv_call.sv 
if test $? -ne 0; then exit 1; fi

vsim -c -do "run -a; quit -f" sv2py2sv_call ${flags}
if test $? -ne 0; then exit 1; fi


