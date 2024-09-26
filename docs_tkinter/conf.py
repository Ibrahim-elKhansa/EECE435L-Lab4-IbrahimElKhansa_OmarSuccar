import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../models'))
sys.path.insert(0, os.path.abspath('../sql'))
sys.path.insert(0, os.path.abspath('../ui'))

project = 'School Management System'
copyright = '2024, Ibrahim El Khansa & Omar Succar'
author = 'Ibrahim El Khansa & Omar Succar'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
