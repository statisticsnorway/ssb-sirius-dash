import logging

import dash_bootstrap_components as dbc
from dash import html

logger = logging.getLogger(__name__)


def format_timespan(start: int | float, end: int | float) -> str:
    """Formats the elapsed time between two time points into a human-readable string.

    Args:
        start (int | float): Start time in seconds, typically as a timestamp or relative value.
        end (int | float): End time in seconds, typically as a timestamp or relative value.

    Returns:
        str: A formatted string representing the elapsed time between `start` and `end`.
        The format is "MM:SS.sss (sss ms)", where:
        - MM is minutes, zero-padded to 2 digits.
        - SS.sss is seconds with 2 decimal places.
        - sss ms represents milliseconds.

    Raises:
        ValueError: If `start` is greater than `end`.
    """
    if start > end:
        raise ValueError("Start time must not be greater than end time.")

    elapsed_time = end - start
    minutes, seconds = divmod(elapsed_time, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(minutes):0>2}:{seconds:05.2f} ({milliseconds:.0f} ms)"


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
