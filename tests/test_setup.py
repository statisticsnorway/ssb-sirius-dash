from ssb_sirius_dash.setup.main_layout import main_layout
import dash_bootstrap_components as dbc

def test_main_layout():
    layout = main_layout([], [], [])
    assert isinstance(layout, dbc.Container), f"main_layout not returning dbc.Container, returns: {type(layout)}"