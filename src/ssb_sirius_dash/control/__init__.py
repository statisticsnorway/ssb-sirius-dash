"""Framework that can be used to create validation checks for the data and creating a quality report."""

import glob
import os

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f) and not f.endswith("__init__.py")
]
