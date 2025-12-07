#!/bin/bash

script_dir=$(dirname $(realpath $0))

if test -z ${PYTHON}; then
    PYTHON=$(which python3)
fi

uvx=$(which uvx)

if test ! -d ${script_dir}/packages; then
  if test ! -z $uvx; then
    echo "Setting up packages directory using uvx ivpm update"
    # Use uvx to initialize the project
    uvx ivpm update
  else
    echo "Setting up packages directory using ${PYTHON}"
    ${PYTHON} -m venv ${script_dir}/packages/python
    ${script_dir}/packages/python/bin/pip install ivpm
    if test $? -ne 0; then exit 1; fi
    ${script_dir}/packages/python/bin/ivpm update -a
    if test $? -ne 0; then exit 1; fi
  fi
else
  echo "Project already bootstrapped"
fi