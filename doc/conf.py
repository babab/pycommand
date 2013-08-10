#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pycommand import __version__ as pycommand_version

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'pycommand'
copyright = '2013, Benjamin Althues'
version = pycommand_version
release = pycommand_version
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'nature'

man_pages = [
    ('index', 'pycommand', 'pycommand Documentation',
     ['Benjamin Althues'], 1)
]

texinfo_documents = [
    ('index', 'pycommand', 'pycommand Documentation',
     'Benjamin Althues', 'pycommand', 'One line description of project.',
     'Miscellaneous'),
]
