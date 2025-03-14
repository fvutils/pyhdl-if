#!/bin/bash

script_dir=$(dirname $(realpath $0))

if test -z ${PYTHON}; then
    PYTHON=$(which python3)
fi


if test ! -d ${script_dir}/packages; then
    echo "Setting up packages directory using ${PYTHON}"
    ${PYTHON} -m venv ${script_dir}/packages/python
    ${script_dir}/packages/python/bin/pip install ivpm
    if test $? -ne 0; then exit 1; fi
    ${script_dir}/packages/python/bin/ivpm update -a
    if test $? -ne 0; then exit 1; fi
else
    echo "Packages directory already exists"
fi