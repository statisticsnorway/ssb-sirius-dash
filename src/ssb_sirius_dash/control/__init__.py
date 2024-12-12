"""Framework that can be used to create validation checks for the data and creating a quality report."""

import importlib
import os
import pkgutil
from collections.abc import Iterator
from typing import Any

current_dir = os.path.dirname(__file__)
__all__: list[str] = []

module_iter: Iterator[tuple[Any, str, bool]] = pkgutil.iter_modules([current_dir])

for _module_finder, module_name, _is_pkg in module_iter:
    module = importlib.import_module(f".{module_name}", package=__name__)
    for attr_name in dir(module):
        if not attr_name.startswith("_"):
            globals()[attr_name] = getattr(module, attr_name)
            __all__.append(attr_name)
