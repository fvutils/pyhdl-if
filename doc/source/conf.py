# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))

source_dir = os.path.dirname(os.path.abspath(__file__))
doc_dir = os.path.dirname(source_dir)
pyhdl_if_dir = os.path.dirname(doc_dir)

sys.path.insert(0, os.path.join(pyhdl_if_dir, "src"))

# -- Project information -----------------------------------------------------

project = 'PyHDL-IF'
copyright = '2024, Matthew Ballance'
author = 'Matthew Ballance'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx_systemverilog',
    'sphinx_rtd_theme',
    'sphinxarg.ext'
]

# -- Python API documentation ------------------------------------------------
# Docstrings are Google style (see doc/documentation-plan.md 5.1); napoleon
# rewrites them into field lists, which is the same shape sphinx-systemverilog
# emits for the SV half, so both halves of the reference render alike.
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Types live in annotations and are never repeated in prose. This folds the
# annotation into the rendered parameter entry so nothing is lost.
autodoc_typehints = "description"
autodoc_member_order = "bysource"

autosummary_generate = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pytest": ("https://docs.pytest.org/en/stable", None),
}

# -- SystemVerilog API documentation -----------------------------------------
# The SV sources are parsed directly by sphinx-systemverilog (via pyslang).
# Named build-unit roots rather than sv_source_dirs: the .svh files are
# `include`-ed into a package, so scanning the directory would parse each
# fragment as its own compilation unit and fail.
sv_dpi_dir = os.path.join(pyhdl_if_dir, "src", "hdl_if", "share", "dpi")
sv_uvm_dir = os.path.join(pyhdl_if_dir, "src", "hdl_if", "share", "uvm")
sv_uvm_lib = os.path.join(pyhdl_if_dir, "packages", "uvm", "src")

sv_doc_style = "doxygen"        # matches the /** ... */ comments in the sources
sv_include_dirs = [sv_dpi_dir, sv_uvm_dir, sv_uvm_lib]

# The pyhdl_uvm package needs the UVM library to elaborate.  That comes from
# ivpm (packages/uvm) and is absent in a bare checkout, so the UVM reference is
# conditional: the 'have_uvm' tag gates the generated section in uvm.rst.
# Set PYHDL_DOCS_NO_UVM=1 to skip it (and the added build time) deliberately.
if (os.path.isfile(os.path.join(sv_uvm_lib, "uvm_pkg.sv"))
        and not os.environ.get("PYHDL_DOCS_NO_UVM")):
    sv_build_units = [
        os.path.join(sv_uvm_lib, "uvm_pkg.sv"),
        os.path.join(sv_dpi_dir, "pyhdl_if.sv"),
        os.path.join(sv_uvm_dir, "pyhdl_uvm.sv"),
    ]
    tags.add("have_uvm")        # noqa: F821 (Sphinx injects `tags`)
else:
    sv_build_units = [os.path.join(sv_dpi_dir, "pyhdl_if.sv")]

# The TLM FIFO interfaces (tlm_hdl2hvl_fifo.sv, tlm_hvl2hdl_fifo.sv) are
# deliberately NOT parsed.  They are instantiated in a design rather than
# `include`-ed into the package, so each would be its own build unit -- but
# their `Closure::invokeTask` implementations do not match the current
# `ICallApi::invokeTask` signature and none of them compiles.  Adding them
# here surfaces two parser errors and breaks the -W build.  Doc comments are
# already written in those files; re-enable this once the signatures are
# fixed.  See doc/documentation-plan.md F19.
#
# sv_build_units += [
#     os.path.join(sv_dpi_dir, "tlm_hdl2hvl_fifo.sv"),
#     os.path.join(sv_dpi_dir, "tlm_hvl2hdl_fifo.sv"),
# ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Copy JSON schema to the root of the build output
html_extra_path = [os.path.join(doc_dir, 'pyhdl-if.schema.json')]
