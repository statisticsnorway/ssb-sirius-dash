import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State
from dash_bootstrap_templates import load_figure_template

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
    @app.callback(
        Output("main-varvelger", "style"),
        Input("sidebar-varvelger-button", "n_clicks"),
        State("main-varvelger", "style"),
    )
    def toggle_varvelger(n_clicks, style):
        if n_clicks > 0:
            if style == {"display": "none"}:
                style = {}
            else:
                style = {"display": "none"}
            return style

    return app