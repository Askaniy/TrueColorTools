"""Shared pytest configuration for TCT tests."""

import os
import tempfile

# Matplotlib must get a writable cache directory before it is imported.
os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='tct-mpl-'))

from truecolortools.core import configure_filter_paths

# The application configures this in `runTCT.py`; tests import the library
# directly, so they must perform the same explicit setup.
configure_filter_paths()
