from dash import html
import dash_bootstrap_components as dbc

from ssb_sirius_dash.utils.functions import sidebar_button

def test_sidebar_button():
    button = sidebar_button("icon","text", "id")
    assert isinstance(button, html.Div)
    assert isinstance(button.children, dbc.Button)