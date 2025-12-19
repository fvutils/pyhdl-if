
# Initializing the Project
After the project is cloned, you must fetch external packages. 
Use the following command to do this. Only do this if the 'packages' 
directory is not present:

```
% ivpm update
```

# Building the Project
There are two steps required to build the native components of
the project:

```
% ./packages/python/bin/python setup.py build_ext --inplace
% ./packages/python/bin/python -m build -n .
```

# Running Tests
Unit tests can be run using the following command:

```
% PYTHONPATH=$(pwd)/src ./packages/python/bin/pytest -s tests/unit
```

# Updating the Python/UVM API
When changing the Python/UVM API, pyhdl_uvm_apis.svh must be re-generated.
The following command does this:

```
% python -m hdl_if api-gen-sv -o src/hdl_if/share/uvm/pyhdl_uvm_apis.svh -m hdl_if.uvm.wrap
```
