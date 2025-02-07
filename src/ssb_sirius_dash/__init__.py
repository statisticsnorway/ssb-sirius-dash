"""SSB Sirius Dash."""

from . import control
from . import modals
from . import setup
from . import tabs
from .kostra_r_wrapper import _get_kostra_r
from .kostra_r_wrapper import hb_method
from .kostra_r_wrapper import th_error

# Re-import functions and classes from submodules explicitly for top-level access
from .setup import main_layout
from .utils.alert_handler import create_alert

# Defines top level if used in wildcard import
__all__ = ["control", "create_alert", "main_layout", "modals", "setup", "tabs"]
