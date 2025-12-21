# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath(".."))  # make your project importable

# -- Project information -----------------------------------------------------

project = "CurrencyConverter"
author = "Tony Narloch"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc", # Used to pull in docstrings automatically
    "sphinx.ext.viewcode", # links to source code in HTML
    "myst_parser," # enables Markdown
    "sphinxcontrib.mermaid" # enables Mermaid
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]
