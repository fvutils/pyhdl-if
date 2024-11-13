DOC_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PYHDL_IF_DIR:=$(abspath $(DOC_DIR)/..)

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

SV_DEPS:=$(shell find $(PYHDL_IF_DIR)/src/hdl_if/share/dpi -name '*.sv*')


#sv_doc : sv_pp.sv
#	echo "test"

pyhdl_if_pp.sv : $(SV_DEPS)
	touch uvm_macros.svh
	verilator -E --pp-comments +incdir+$(PYHDL_IF_DIR)/src/hdl_if/share/dpi \
		+incdir+$(pwd) \
		$(PYHDL_IF_DIR)/src/hdl_if/share/dpi/pyhdl_if.sv > $@ || rm -f $@

pyhdl_if_uvm_pp.sv : $(SV_DEPS)
	touch uvm_macros.svh
	verilator -E --pp-comments +incdir+$(PYHDL_IF_DIR)/src/hdl_if/share/dpi \
		+incdir+$(pwd) \
		$(PYHDL_IF_DIR)/src/hdl_if/share/dpi/pyhdl_if_uvm.sv > $@ || rm -f $@

pyhdl_if.cpp : pyhdl_if_pp.sv pyhdl_if_uvm_pp.sv
#	echo "namespace pyhdl_if {" > $@
	perl $(PYHDL_IF_DIR)/packages/doxygen-filter-sv/filter/idv_doxyfilter_sv.pl \
		pyhdl_if_pp.sv >> $@ || rm -f $@
#	echo "} // namespace pyhdl_if" >> $@
#	echo "namespace pyhdl_if_uvm {" >> $@
#	perl $(PYHDL_IF_DIR)/packages/doxygen-filter-sv/filter/idv_doxyfilter_sv.pl \
#		pyhdl_if_uvm_pp.sv >> $@ || rm -f $@
#	echo "} // namespace pyhdl_if_uvm" >> $@
	sed -i -e 's/automatic//g' $@ -e 's/\[\$$\]/[]/g' -e 's/longint unsigned/unsigned long long/g'

pyhdl_if_doxy.d : pyhdl_if.cpp
	rm -rf pyhdl_if_doxy
	doxygen Doxyfile
	cd pyhdl_if_doxy/xml ; for file in *.xml; do sed -i -e 's/inline="yes"/inline="no"/g' $$file; done
	touch $@

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile pyhdl_if_doxy.d
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean :
	rm -rf pyhdl_if_doxy pyhdl_if_doxy.d pyhdl_if_pp.sv pyhdl_if_uvm_pp.sv uvm_macros.svh
	rm -rf pyhdl_if.cpp html build
