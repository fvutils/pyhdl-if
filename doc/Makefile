# Minimal makefile for Sphinx documentation
#
# The SystemVerilog API reference is produced by the sphinx-systemverilog
# extension, which parses the SV sources directly (see source/conf.py).
# No preprocessing, filtering, or Doxygen pass is required.

# You can set these variables from the command line, and also
# from the environment for the first two.
# Warnings are errors: the reference is generated, so a warning means an
# object went missing or a reference broke.  --keep-going reports every
# problem in one run rather than stopping at the first.
SPHINXOPTS    ?= -W --keep-going
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Not part of `html`: it needs network access and third-party sites go down
# for reasons that have nothing to do with this repository.
linkcheck: Makefile
	@$(SPHINXBUILD) -M linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(O)

clean :
	rm -rf build

.PHONY: help html linkcheck clean
