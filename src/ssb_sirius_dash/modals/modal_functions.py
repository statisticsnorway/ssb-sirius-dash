import dash_bootstrap_components as dbc
from dash import html


def sidebar_button(
    icon: str,
    text: str,
    component_id: str,
    additional_styling: dict[str, str] | None = None,
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
