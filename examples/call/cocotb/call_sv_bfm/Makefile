TOPLEVEL_LANG ?= verilog
SIM ?= verilator

PWD=$(shell pwd)

HDL_IF_ENTRY := $(shell python -c "import hdl_if; print(hdl_if.get_entry())")
HDL_IF_SHARE := $(shell python -c "import hdl_if; print(hdl_if.share())")

VERILOG_SOURCES += $(HDL_IF_SHARE)/dpi/pyhdl_if.sv
VERILOG_SOURCES += $(PWD)/call_sv_bfm.sv

TOPLEVEL := call_sv_bfm
MODULE   := call_sv_bfm

EXTRA_ARGS += --timing +incdir+${HDL_IF_SHARE}/dpi --vpi -Wno-fatal -LDFLAGS -export-dynamic  -LDFLAGS ${HDL_IF_ENTRY}

include $(shell cocotb-config --makefiles)/Makefile.sim
