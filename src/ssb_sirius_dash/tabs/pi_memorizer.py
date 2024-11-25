import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from mpmath import mp

mp.dps = 1000

pi = str(mp.pi)


class PimemorizerTab:
    def __init__(
        self,
    ):
        self.label = "𝝅 Pi memorizer"
        self.callbacks()

    def layout(self):
        layout = html.Div(
            style={"display": "grid", "grid-template-columns": "10% 70% 10% 10%"},
            children=[
                html.Div(),
                    html.Div(
                        [
                        html.Div(
                            style={"margin-bottom": "20px"},
                            children=[
                                dbc.Textarea(
                                    id="text-box",
                                    size="xxl",
                                    value="3.",
                                ),
                            ]
                        ),

                        html.Div(
                            style={"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "10px", "justify-content": "center"},
                            children=[
                                dbc.Button("1", id="pi-button1", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("2", id="pi-button2", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("3", id="pi-button3", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("4", id="pi-button4", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("5", id="pi-button5", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("6", id="pi-button6", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("7", id="pi-button7", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("8", id="pi-button8", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("9", id="pi-button9", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("", id="pi-button-empty1", color="secondary", disabled=True, style={"font-size": "20px", "padding": "20px", "grid-column": "span 1"}),
                                dbc.Button("0", id="pi-button0", color="primary", style={"font-size": "20px", "padding": "20px"}),
                                dbc.Button("", id="pi-button-empty2", color="secondary", disabled=True, style={"font-size": "20px", "padding": "20px", "grid-column": "span 1"}),
                            ]
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Score", className="card-title"),
                                    html.Div(
                                        style={
                                            "display": "grid",
                                            "grid-template-columns": "100%",
                                        },
                                        children=[
                                            dbc.Input(value=0, id="score", type="number"),
                                        ],
                                    ),
                                ],
                                style={"max-height": "100%"},
                            ),
                            style={"max-height": "100%"},
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("High score", className="card-title"),
                                    html.Div(
                                        style={
                                            "display": "grid",
                                            "grid-template-columns": "100%",
                                        },
                                        children=[
                                            dbc.Input(value=0, id="highscore", type="number"),
                                        ],
                                    ),
                                ],
                                style={"max-height": "100%"},
                            ),
                            style={"max-height": "100%"},
                        )
                    ]
                ),
                html.Div(),
            ]
        )
        return layout

    def callbacks(self):
        @callback(
            Output("text-box", "value"),
            Output("score", "value"),
            Output("highscore", "value"),
            Input("pi-button0", "n_clicks"),
            Input("pi-button1", "n_clicks"),
            Input("pi-button2", "n_clicks"),
            Input("pi-button3", "n_clicks"),
            Input("pi-button4", "n_clicks"),
            Input("pi-button5", "n_clicks"),
            Input("pi-button6", "n_clicks"),
            Input("pi-button7", "n_clicks"),
            Input("pi-button8", "n_clicks"),
            Input("pi-button9", "n_clicks"),
            State("score", "value"),
            State("highscore", "value"),
            State("text-box", "value"),
        )
        def update_input(btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, current_score, high_score, current_value):
            current_value = current_value or ""
            current_score = current_score or 0

            ctx = callback_context
            if not ctx.triggered:
                return current_value, current_score

            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if button_id.startswith("pi-button"):
                number = button_id[-1]
                new_string = current_value + number

            if new_string == pi[:int(current_score)+3]:
                new_score = current_score + 1
                return new_string, new_score, high_score
            else:
                if current_score > high_score:
                    high_score = current_score
                current_value = "3."
                current_score = 0
                return current_value, current_score, high_score
