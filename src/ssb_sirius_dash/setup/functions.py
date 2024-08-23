import dash_bootstrap_components as dbc
from dash import html

def skjermcard(text, component_id, input_type, value=None):
    if value is None:
        value = ""
    card = dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(text, className="card-title"),
                    html.Div(
                        style={
                            "display": "grid",
                            "grid-template-columns": "100%",
                        },
                        children=[
                            dbc.Input(value=value, id=component_id, type=input_type),
                        ],
                    ),
                ],
                style={"max-height": "100%"},
            ),
        style={"max-height": "100%"},
        )
    )
    return card

def sidebar_button(icon, text, component_id, additional_styling=None):
    if additional_styling is None:
        additional_styling = {}
    button = html.Div(
        dbc.Button(
            [
                html.Span(icon, style={"display": "block", "font-size": "1.4rem"}),
                html.Span(text, style={"display": "block", "font-size": "0.7rem"}),
            ],
            id=component_id,
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "word-break": "break-all",
                "margin-bottom": "5%",
                "width": "100%",
                **additional_styling,
            },
        )
    )
    return button


def card_display(text, component_id):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(text, className="card-title"),
                    html.Span(id=component_id, style={"display": "block"}),
                ],
                style={"max-height": "100%"},
            )
        ],
        style={"max-height": "100%"},
    )
    return card


def card_navigate(icon, text, component_id):
    card = dbc.Card(
        [dbc.CardBody([sidebar_button(icon, text, component_id)])],
        inverse=True,
    )
    return card
