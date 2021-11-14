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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Imports ----------------

import sphinx_readable_theme

# -- Project information -----------------------------------------------------

project = 'PyDataStructs'
copyright = '2021, PyDataStructs Development Team'
author = 'PyDataStructs Development Team'
master_doc = 'index'

# The full version, including alpha/beta/rc tags
release = '1.0.1-dev'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_nb'
]

jupyter_execute_notebooks = "off"

napoleon_numpy_docstring = True

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'readable'

html_theme_path = [sphinx_readable_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

autodoc_default_options = {
    'member-order': 'bysource',
    'members': True,
    'undoc-members': True,
    'special-members': True,
    'exclude-members': '__new__, methods, __slots__, __dict__, __weakref__'
}
