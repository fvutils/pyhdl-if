# PyHDL-IF - A Python Interface to HDL Simulators

PyHDL-IF implements several interfaces between Python and 
hardware description languages, with a current focus on SystemVerilog.
- Start Python behavior from SystemVerilog/UVM, and interact with UVM classes
- Call SystemVerilog functions and tasks from Python, and invoke Python methods from SystemVerilog
- Use the Python C API, and a SystemVerilog convenience API, to call Python
- **Run async pytest tests from SystemVerilog testbenches**

## Key Features

### Pytest Runner
Run async Python tests directly from SystemVerilog testbenches with pytest's assertion rewriting:

```systemverilog
module my_test;
    initial begin
        pyhdl_if::pyhdl_if_start();
        pyhdl_if::pyhdl_pytest("tests/my_async_tests.py");
        $finish;
    end
endmodule
```

See [doc/pytest_runner.md](doc/pytest_runner.md) for complete documentation and examples.

## Installing PyHDL-IF
Installing PyHDL-IF in your own Python virtual environment is easy:

```
% pip install pyhdl-if
```

Binary wheels are currently available for Linux x86_64 platforms.

# Running Examples
See [Examples.md](examples/Examples.md) for instructions on how to run examples.


## Setting up a Development Environment

PyHDL-IF uses [IVPM](https://fvutils.github.io/ivpm/) to manage dependencies. The
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

By default, all available simulators supported by a given test will be run. 
You can filter the simulators to run using the pytest `-k` option.
- mti - Siemens Questa (Modeltech)
- xcm - Cadence Xcelium
- vcs - Synopsys VCS
- vlt - Verilator

```
%  PYTHONPATH=$(pwd)/src ./packages/python/bin/python3 -m pytest -s tests/ -k [vlt]
```

The command above runs tests with Verilator only.




