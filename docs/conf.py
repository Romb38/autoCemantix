import os
import sys
from datetime import datetime

# Add source code path
sys.path.insert(0, os.path.abspath('..'))

project = os.getenv("PROJECT_NAME", "DefaultProjectName")
author = "Romb38"
release = "0.1.0"
year = datetime.now().year

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",  # pour supporter le README.md
]
myst_suppress_warnings = ["myst.header"]

# Fichiers source supportés (rst + md)
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# README.md comme page d'accueil
master_doc = 'index'

# HTML theme
html_theme = "sphinx_rtd_theme"

# Inclure les docstrings de __init__.py
autoclass_content = "class"
add_module_names = False

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

