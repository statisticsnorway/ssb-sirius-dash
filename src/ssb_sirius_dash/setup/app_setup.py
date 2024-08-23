import os
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Dash

theme_map = {
    "sketchy": dbc.themes.SKETCHY,
    "slate": dbc.themes.SLATE,
    "cyborg": dbc.themes.CYBORG,
    "superhero": dbc.themes.SUPERHERO,
    "darkly": dbc.themes.DARKLY,
    "solar": dbc.themes.SOLAR,
    "flatly": dbc.themes.FLATLY,
}


def app_setup(port, service_prefix, domain, stylesheet):
    template = theme_map[stylesheet]
    load_figure_template([template])

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = Dash(
        __name__,
        requests_pathname_prefix=f"{service_prefix}proxy/{port}/",
        external_stylesheets=[theme_map[stylesheet], dbc_css],
    )
    return app