"""SSB Sirius Dash."""

# Import all Python files in the root of ssb_sirius_dash
import glob
import os

# Automatically import all .py files in the current directory (excluding __init__.py)
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f) and not f.endswith("__init__.py")
]

# Import submodules explicitly for clarity
from . import control
from . import modals
from . import setup
from . import tabs
