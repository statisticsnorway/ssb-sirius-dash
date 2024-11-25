import dash_bootstrap_components as dbc
from dash import html
from .functions import sidebar_button


def main_layout(modal_list, tab_list, variable_list):
    varvelger_toggle = [
        html.Div(
            [
                sidebar_button("🛆", "vis/skjul variabelvelger", "sidebar-varvelger-button")
            ]
        )
    ]
    modal_list = varvelger_toggle + modal_list
    selected_tab_list = [dbc.Tab(tab.layout(), label=tab.label) for tab in tab_list]
    layout = dbc.Container(
        [
            html.Div(
                id="notifications-container",
                style={"position": "fixed", "z-index": 9999},
            ),
            html.P(
                id="update-status", style={"font-size": "60%", "visibility": "hidden"}
            ),
            html.Div(
                id="main-layout",
                style={
                    "height": "100vh",
                    "overflow": "hidden",
                    "display": "grid",
                    "grid-template-columns": "5% 95%",
                },
                children=[
                    html.Div(
                        className="bg-secondary",
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            "height": "100%",
                        },
                        children=modal_list,
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                dbc.Row(children=variable_list),
                                style={"display": "none"},
                                id="main-varvelger",
                            ),
                            html.Div(
                                dbc.Tabs(
                                    selected_tab_list,
                                ),
                            )
                        ],
                    ),
                ],
            ),
        ],
        fluid=True,
        className="dbc dbc-ag-grid",
    )
    return layout