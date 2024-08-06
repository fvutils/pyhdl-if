#!/bin/sh -x

echo "BUILD_NUM=${BUILD_NUM}" >> src/hdl_if/__build_num__.py
${IVPM_PYTHON} -m pip install ivpm cython
${IVPM_PYTHON} -m ivpm update -a

PYTHON=./packages/python/bin/python
${PYTHON} -m pip install twine auditwheel ninja wheel cython
${PYTHON} setup.py bdist_wheel

for whl in dist/*.whl; do
    ${PYTHON} -m auditwheel repair $whl
    rm $whl
done