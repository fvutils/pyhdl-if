#!/bin/sh

export PYTHONPATH=`pwd`/../../../src:.:${PYTHONPATH}

share_pi=$(python3 -c 'import hdl_pi_if; print(hdl_pi_if.share())')
share_call=$(python3 -c 'import hdl_call_if; print(hdl_call_if.share())')
libs=$(python3 -c 'import hdl_pi_if; print(" ".join(hdl_pi_if.libs()))')
python_libdir=$(python3 -c 'import sysconfig, os; print(os.path.join(sysconfig.get_config_var("installed_platbase"), "lib"))')

python3 -m hdl_call_if gen-sv -m sv2py_call -o MyC.svh
if test $? -ne 0; then exit 1; fi

echo "share_call: '${share_call}'"

verilator --binary \
	+incdir+${share_pi}/dpi \
	+incdir+${share_call}/dpi \
	${share_pi}/dpi/pyhdl_dpi_if.sv \
	${share_call}/sv/pyhdl_call_if.sv \
	sv2py_call.sv -top sv2py_call \
	${libs} -LDFLAGS -Wl,--export-dynamic -LDFLAGS -Wl,-rpath,${python_libdir}
if test $? -ne 0; then exit 1; fi

./obj_dir/Vsv2py_call

