# Example: cocotb/call_sv_bfm

This example highlights interoperability between cocotb and PyHDL-IF. The Python testbench (call_sv_bfm.py)
interacts with clock and reset signals using cocotb, then interacts via tasks with a bus functional model (BFM)
implemented in SystemVerilog.

## How to Run
1. Download docker and build the image using the dockerfile in the project root
```
	docker build -t local_test . # Run this in proj root dir
```

2. Get an interactive terminal to the docker container and mount our work area so changes persist when the container shuts down
```
	docker run -it -v "$(pwd)":/work/pyhdl-if local_test /bin/bash # run this in proj root dir
```

3. `cd` to example directory inside the docker container, initialize the venv and activate it
```
	cd pyhdl-if/examples/call/cocotb/call_sv_bfm/
	./init_venv.sh
	source example_venv/bin/activate
```

4. Run the test
```
	make
```
