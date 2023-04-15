import os
import sys

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinxarg.ext',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

source_suffix = '.rst'
master_doc = 'index'

project = 'sr.comp.cli'
copyright = '2015-2023, SRComp contributors'  # noqa: A001

html_theme = 'alabaster'

intersphinx_mapping = {'http://docs.python.org/': None}
