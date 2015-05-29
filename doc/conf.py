#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycommand

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'pycommand'
copyright = '2013-2015, Benjamin Althues'
version = pycommand.__version__
release = pycommand.__version__
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'nature'

man_pages = [
    ('index', 'pycommand', 'pycommand Documentation',
     ['Benjamin Althues'], 3)
]

texinfo_documents = [
    ('index', 'pycommand', 'pycommand Documentation',
     'Benjamin Althues', 'pycommand', pycommand.__doc__,
     'Miscellaneous'),
]
