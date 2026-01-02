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
#    'sphinx.ext.ingmath', 
    'sphinx.ext.todo', 
    'sphinx.ext.autodoc',
    'breathe',
    'sphinx_rtd_theme',
    'sphinxarg.ext'
]

breathe_projects = {
    "pyhdl_if": os.path.join(doc_dir, "pyhdl_if_doxy", "xml")
}
breathe_default_project = "pyhdl_if"
breathe_implementation_filename_extensions = []

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
