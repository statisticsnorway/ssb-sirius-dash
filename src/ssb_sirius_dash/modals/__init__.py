"""Modals for use in the application."""

import importlib
import os
import pkgutil

current_dir = os.path.dirname(__file__)
__all__ = []

for _, module_name, _ in pkgutil.iter_modules([current_dir]):
    module = importlib.import_module(f".{module_name}", package=__name__)
    for attr_name in dir(module):
        if not attr_name.startswith("_"):
            globals()[attr_name] = getattr(module, attr_name)
            __all__.append(attr_name)
