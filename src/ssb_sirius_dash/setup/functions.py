import dash_bootstrap_components as dbc
from dash import html


def skjermcard(
    text: str, component_id: str, input_type: str, value: str | None = None
) -> dbc.Col:
    """Generate a Dash Bootstrap card with an input field.

    Parameters
    ----------
    text : str
        The title text displayed on the card.
    component_id : str
        The ID assigned to the input component inside the card.
    input_type : str
        The type of the input field (e.g., "text", "number").
    value : str, optional
        The default value for the input field. Defaults to an empty string.

    Returns:
    --------
    dash_bootstrap_components.Col
        A column containing the card with an input field.
    """
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


def sidebar_button(
    icon: str, text: str, component_id: str, additional_styling: dict | None = None
) -> html.Div:
    """Generate a sidebar button with an icon and label.

    Parameters
    ----------
    icon : str
        The icon displayed at the top of the button.
    text : str
        The label text displayed below the icon.
    component_id : str
        The ID assigned to the button component.
    additional_styling : dict, optional
        Additional styling applied to the button. Defaults to an empty dictionary.

    Returns:
    --------
    dash.html.Div
        A Div containing the styled button.
    """
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


def card_display(text: str, component_id: str) -> dbc.Card:
    """Generate a Dash Bootstrap card for displaying text content.

    Parameters
    ----------
    text : str
        The title text displayed on the card.
    component_id : str
        The ID assigned to the text span inside the card.

    Returns:
    --------
    dash_bootstrap_components.Card
        A card containing the text content.
    """
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


def card_navigate(icon: str, text: str, component_id: str) -> dbc.Card:
    """Generate a navigational card with a button.

    Parameters
    ----------
    icon : str
        The icon displayed on the button inside the card.
    text : str
        The label text displayed on the button inside the card.
    component_id : str
        The ID assigned to the button component.

    Returns:
    --------
    dash_bootstrap_components.Card
        A card containing the button for navigation.
    """
    card = dbc.Card(
        [dbc.CardBody([sidebar_button(icon, text, component_id)])],
        inverse=True,
    )
    return card
