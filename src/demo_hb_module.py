# +
import os
print(os.getcwd())
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from ssb_sirius_dash.hb_module_aio import hb

port = 8063
service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)

app = Dash(
    __name__,
    requests_pathname_prefix=f"{service_prefix}proxy/{port}/",
    external_stylesheets=[
        dbc.themes.DARKLY,
        # "https://unpkg.com/@mantine/notifications@7/styles.css",# Står i dokumentasjon at dette trengs, men det slutter å fungere når den er med. Sannsynligvis er dokumentasjon utdatert: https://www.dash-mantine-components.com/migration#required-stylesheets
    ],
)

app.layout=html.Div([dcc.Dropdown(id="selector"), dcc.Dropdown(id="identifikator"),hb(hotkey="b")])

if __name__ == "__main__":
    app.run(debug=True, port=port, jupyter_server_url=domain, jupyter_mode="tab")
# -


