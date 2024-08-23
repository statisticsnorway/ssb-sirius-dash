import dash_bootstrap_components as dbc
from dash import html

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