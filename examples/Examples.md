
# PyHDL-IF Examples

Several Python packages, and a simulation tool, need to be
available in order to run the examples. There are several paths
for doing this, as described below.

## Using Tool Setup Script
The 'setup.sh' script in the examples directory configures a 
standalone tool environment that contains tools to run the examples
using open source simulation tools (Verilator). This tool installation 
can also be used to run the examples with a closed-source simulation tool.

```bash
Usage: ./examples/setup.sh [options] [tools_dir]

Arguments:
  tools_dir                Directory in which to create tools (default: $PWD/hdl_if_tools)

Options:
  -d, --dev-pkgs           Install dv-flow-mgr, dv-flow-libhdlsim, and pyhdl-if from development sources
  -w, --pyhdl-wheel PATH   Path to a Python wheel to install for pyhdl-if instead of the PyPi version
  -h, --help, -?, -help    Print this help message
```

After running setup.sh, you can source <tool_dir>/setup.[c]sh to configure 
environment variables.

### Using a PyHDL-IF development environment

Follow the instructions for setting up a development environment with
`ivpm`. This will install dependencies, including Verilator, in the 'packages' 
directory in the project root. `direnv` will ensure that the proper paths
are added to the environment.

### Setting up a standalone environment

Install the following Python packages:
- pyhdl-if
- dv-flow-mgr
- dv-flow-libhdlsim

Make available at least one of the following simulators:
- Verilator (5.043+) (vlt)
  - Note: Verilator does not run the UVM examples at this time
- Cadence Xcelium (xcm)
- Siemens Questa (mti)
- Synopsys VCS (vcs)

## Running an Example
Examples are run via the DV Flow Manager (dfm) tool. You can specify the 
simulator to use via the -Dsim=<sim> option. Most examples can be run
like this:

```
% dfm run -Dsim=<sim> sim-run
```

Output data is found in the `rundir` subdirectory of the example. 
- rundir/<example-name>.sim-run/sim.log - simulation logfile

You can see the detailed commands used to run the example by running:

```
% dfm --log-level=INFO run -Dsim=<sim> sim-run
```


