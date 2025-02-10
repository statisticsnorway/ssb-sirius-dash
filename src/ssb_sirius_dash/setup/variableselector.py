import logging
from typing import Any

import dash_bootstrap_components as dbc
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html

# +
# from ..utils.alert_handler import create_alert
# -

logger = logging.getLogger(__name__)
variable_options = {
    "aar": {"title": "År", "id": "var-aar", "type": "number"},
    "termin": {"title": "Termin", "id": "var-termin", "type": "number"},
    "maaned": {"title": "Måned", "id": "var-maaned", "type": "number"},
    "nace": {"title": "Nace", "id": "var-nace", "type": "text"},
    "oppgavegiver": {"title": "Oppgavegiver", "id": "var-oppgavegiver", "type": "text"},
    "foretak": {"title": "Foretak", "id": "var-foretak", "type": "text"},
    "bedrift": {"title": "Bedrift", "id": "var-bedrift", "type": "text"},
    "fylke": {"title": "Fylke", "id": "var-fylke", "type": "text"},
    "skjemaenhet": {"title": "Skjemaenhet", "id": "var-skjemaenhet", "type": "text"},
    "prodcomkode": {"title": "Prodcomkode", "id": "var-prodcomkode", "type": "text"},
    "nspekfelt": {"title": "NSPEK-felt", "id": "var-nspekfelt", "type": "text"},
}


# +
class VariableSelector:
    """Singleton"""

    _variableselectoroptions = []

    def __str__(self):
        return ("Current options:\n") + self._variableselectoroptions[0].__str__()


class VariableSelectorOption:

    def __init__(
        self, variable_name, variable_title, variable_id, variable_type, input_state
    ):
        self.name = variable_name
        self.title = variable_title
        self.id = variable_id
        self.type = variable_type
        self.input_state = input_state

        VariableSelector._variableselectoroptions.append(self)

    def is_valid(self):
        pass

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Title: {self.title}\n"
            f"Id: {self.id}\n"
            f"Type: {self.type}\n"
            f"input_state: {self.input_state}"
        )

    @staticmethod
    def variableoptionstocallback():
        """Add this inside the @callback(*VariableSelectorOption.variableoptionstocallback())"""
        return [
            Input(VariableOption.id, "value")
            for VariableOption in VariableSelectorOption._variableselectoroptions
            if VariableOption.input_state == "Input"
        ] + [
            State(VariableOption.id, "value")
            for VariableOption in VariableSelectorOption._variableselectoroptions
            if VariableOption.input_state == "State"
        ]


# -

VariableSelectorOption("orgf", "Organisasjonsnummer", "var-orgf", "text", "Input")
VariableSelectorOption("aar", "År", "var-aar", "number", "State")
VariableSelectorOption("nace", "Nace", "var-nace", "text", "State")

VariableSelector._variableselectoroptions

print(VariableSelector())

print(VariableSelector._variableselectoroptions[0])

VariableSelectorOption.variableoptionstocallback()


def create_variable_card(
    text: str,
    component_id: str,
    input_type: str,
    value: str | int | float | None = None,
) -> dbc.Col:
    """Generate a Dash Bootstrap card with an input field.

    Args:
        text (str): The title text to display on the card.
        component_id (str): The ID to assign to the input field within the card.
        input_type (str): The type of the input field (e.g., "text", "number").
        value (str, optional): The default value for the input field. Defaults to an empty string.

    Returns:
        dbc.Col: A column containing the card with an input field.
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
    _make_alert_callback(
        component_id, text
    )  # Should be made optional, maybe as an argument in main_layout
    return card


def _make_alert_callback(component_id: str, component_name: str) -> Any:
    """Utility function to add alerts to updates on the variable selector."""

    @callback(  # type: ignore[misc]
        Output("alert_store", "data", allow_duplicate=True),
        Input(component_id, "value"),
        State("alert_store", "data"),
        prevent_initial_call=True,
    )
    def alert_connection(
        value: Any, error_log: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Alert callback connecting variable picker card to the alert handler."""
        error_log.append(
            create_alert(
                f"Oppdatering av variabelvelger: {component_name} til {value}",
                "info",
                ephemeral=True,
            )
        )
        return error_log

    alert_connection.__name__ = f"alert_connection_{component_id}"
    return alert_connection


def create_variable_selector_content(
    selected_keys: list[str], default_values: dict[str, str | float | int] | None = None
) -> list[dbc.Col]:
    """Generate a list of Dash Bootstrap cards based on selected variable keys.

    Args:
        selected_keys (list[str]): Keys representing variables to include as cards. Each key corresponds
                                   to an entry in the `variable_options` dictionary.
        default_values (dict, optional): A dictionary containing default values for the cards, where the keys
                                         are variable names, and the values are the default input values.
                                         Defaults to an empty dictionary.

    Returns:
        list[dbc.Col]: A list of cards, each represented as a Dash Bootstrap column.

    Raises:
        KeyError: If any required key ('title', 'id', 'type') is missing in `variable_options` for a selected key.
        ValueError: If the `value` provided in `default_values` is not of a supported type.


    Notes:
        - The `variable_options` dictionary provides configuration for each card, including its title, ID, and type.
        - If `selected_keys` includes keys not found in `variable_options`, those keys are ignored.
    """
    if default_values is None:
        default_values = {}
    cards_list = []
    for key in selected_keys:
        card_config = variable_options.get(key)
        if card_config is None:
            raise KeyError(
                f"Key '{key}' not found in variable_options. Accepted values are: {variable_options.keys()}"
            )

        title = card_config.get("title")
        if title is None:
            raise KeyError(f"Key 'title' is missing in configuration for '{key}'")
        card_id = card_config.get("id")
        if card_id is None:
            raise KeyError(f"Key 'id' is missing in configuration for '{key}'")
        card_type = card_config.get("type")
        if card_type is None:
            raise KeyError(f"Key 'type' is missing in configuration for '{key}'")
        value = default_values.get(key, None)
        if value is not None and not isinstance(value, (str | float | int)):
            raise ValueError(
                f"Value for '{key}' must be of type str, float or int. Got {type(value).__name__}"
            )

        card = create_variable_card(
            text=title, component_id=card_id, input_type=card_type, value=value
        )
        cards_list.append(card)
    return cards_list
