"""SSB Sirius Dash."""
import os
import importlib

# Path to the src folder
src_dir = os.path.dirname(__file__)

# Traverse the modules in the ssb-sirius-dash directory
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".py") and not file.startswith("_"):
            module_name = os.path.splitext(file)[0]
            module_path = os.path.relpath(os.path.join(root, file), src_dir)
            module_path = module_path.replace(os.sep, ".").replace(".py", "")

            # Import the module dynamically
            module = importlib.import_module(f".{module_path}", package="ssb_sirius_dash")

            # Get all attributes that don't start with "_"
            for attr_name in dir(module):
                if not attr_name.startswith("_"):
                    globals()[attr_name] = getattr(module, attr_name)
