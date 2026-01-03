#!/bin/sh -x

echo "BUILD_NUM=${BUILD_NUM}" > src/hdl_if/__build_num__.py
${IVPM_PYTHON} -m pip install ivpm cython
if test $? -ne 0; then exit 1; fi

${IVPM_PYTHON} -m ivpm update -a -d default-ci
if test $? -ne 0; then exit 1; fi

PYTHON=./packages/python/bin/python
${PYTHON} -m pip install twine auditwheel ninja wheel cython
if test $? -ne 0; then exit 1; fi

${PYTHON} setup.py bdist_wheel
if test $? -ne 0; then exit 1; fi

for whl in dist/*.whl; do
    ${PYTHON} -m auditwheel repair $whl
    if test $? -ne 0; then exit 1; fi
    rm $whl
done