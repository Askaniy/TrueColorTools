"""Shared pytest configuration for TCT tests."""

import os
import tempfile

# Matplotlib must get a writable cache directory before it is imported.
os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='tct-mpl-'))
