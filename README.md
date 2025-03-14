# PyHDL-IF - A Python Interface to HDL Simulators

## Installing PyHDL-IF
As an end user, the easiest way to install PyHDL-IF is via `pip`:

```
% pip install pyhdl-if
```

Binary wheels are currently available for Linux x86_64 platforms.

## Setting up a Development Environment

PyHDL-IF uses (IVPM)[https://fvutils.github.io/ivpm/] to manage dependencies. The
`bootstrap.sh` creates a local Python virtual environment, installs IVPM, and
required fetches packages.

```
% ./bootstrap.sh
```

### Building PyHDL-IF
For development builds, PyHDL-IF is built using the Python `setup.py` script. 
Run the `setup.py` script using the local Python virtual environment:

```
% ./packages/python/bin/python setup.py build_ext --inplace
```

### Running Tests
PyHDL-IF has a growing set of unit tests. These tests assume that you have a
recent version of the [Verilator](https://github.com/verilator/verilator) 
SystemVerilog simulator installed. 

PyHDL-IF uses pytest for its tests. Run the suite of tests like this:

```
% PYTHONPATH=$(pwd)/src ./packages/python/bin/python3 -m pytest -s tests/unit
```

Note: this assumes running `bash` as the shell.

By default, Verilator will be used as the simulator. You can select a different
simulator using the `PYTEST_FV_HDLSIM' environment variable:
- mti - Siemens Questa (Modeltech)
- xcm - Cadence Xcelium
- vcs - Synopsys VCS
- vlt - Verilator

```
% PYTEST_FV_HDLSIM=vlt PYTHONPATH=$(pwd)/src ./packages/python/bin/python3 -m pytest -s tests/
```




