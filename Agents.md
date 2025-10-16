
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