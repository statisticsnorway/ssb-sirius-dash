import dash_bootstrap_components as dbc
from dash import html


def sidebar_button(
    icon: str,
    text: str,
    component_id: str,
    additional_styling: dict[str, str] | None = None,
) -> html.Div:
    """Generate a sidebar button with an icon and label.

    Args:
        icon (str): The icon displayed at the top of the button.
        text (str): The label text displayed below the icon.
        component_id (str): The ID assigned to the button component.
        additional_styling (dict, optional): Additional styling applied to the button. Defaults to an empty dictionary.

    Returns:
        html.Div: A Div containing the styled button.
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

    Args:
        text (str): The title text displayed on the card.
        component_id (str): The ID assigned to the text span inside the card.

    Returns:
        dbc.Card: A card containing the text content.
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

    Args:
        icon (str): The icon displayed on the button inside the card.
        text (str): The label text displayed on the button inside the card.
        component_id (str): The ID assigned to the button component.

    Returns:
        dbc.Card: A card containing the button for navigation.
    """
    card = dbc.Card(
        [dbc.CardBody([sidebar_button(icon, text, component_id)])],
        inverse=True,
    )
    return card
