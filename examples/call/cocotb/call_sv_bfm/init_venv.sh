#!/bin/sh

example_dir=$(dirname $(realpath $0))
rundir=`pwd`

pyhdl_if_dir=$(cd ${example_dir}/../../../../; pwd)


interp_bindir=$rundir/example_venv/bin
interp=$interp_bindir/python
if test ! -d $rundir/example_venv; then
    echo "Creating Python virtual environment"
    python3 -m venv $rundir/example_venv
    $interp -m pip install --upgrade pip
    $interp -m pip install pcpp cxxheaderparser ivpm
    $interp -m pip install -e ${pyhdl_if_dir} cocotb
    $interp -m pip install -r $example_dir/requirements.txt
fi

