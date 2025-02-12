import logging
from typing import Any

import dash_bootstrap_components as dbc
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html

from ..utils.alert_handler import create_alert

logger = logging.getLogger(__name__)


class VariableSelector:
    """Bruk setters og getters to make class usable for functions.
    """
    _variableselectoroptions = []

    def __init__(self, selected_inputs, selected_states, default_values = None):
        self.options = [option.title for option in self._variableselectoroptions]
        self.inputs = [
            Input(option.id, "value")
            for option in self._variableselectoroptions
            if option.title in selected_inputs
        ]
        self.states = [
            State(option.id, "value")
            for option in self._variableselectoroptions
            if option.title in selected_states
        ]
        self.selected_variables = [*selected_inputs, *selected_states]
        self.default_values = default_values

        #self.is_valid()
        
        #if default_values:
        #    self.default_values_is_valid()


    def is_valid(self):
        """Not working atm"""
        valid_options = [x.title for x in self._variableselectoroptions]
        for selected_input in self.inputs:
            if selected_input not in valid_options:
                raise ValueError(
                    f"Received {selected_input}, expected one of {valid_options}"
                )
        for selected_state in self.states:
            if selected_state not in valid_options:
                raise ValueError(
                    f"Received {selected_state}, expected one of {valid_options}"
                )

    def default_values_is_valid(self):
        pass

    def get_option(self, variable_name):
        for option in self._variableselectoroptions:
            if option.title == variable_name:
                return option
    
    def get_callback_components(self):
        return [*self.inputs, *self.states]

    def get_callback_args(self):
        return self.selected_variables


    def _create_variable_card(
        self,
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
                                dbc.Input(
                                    value=value, id=component_id, type=input_type
                                ),
                            ],
                        ),
                    ],
                    style={"max-height": "100%"},
                ),
                style={"max-height": "100%"},
            )
        )
        self._make_alert_callback(
            component_id, text
        )  # Should be made optional, maybe as an argument in main_layout
        return card

    def _make_alert_callback(self, component_id: str, component_name: str) -> Any:
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

    def layout(self,
#        selected_keys: list[str],
#        default_values: dict[str, str | float | int] | None = None,
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
        if self.default_values is None:
            default_values = {}
        else:
            default_values = self.default_values
        layout = []
        for variable in self.selected_variables:
            option = self.get_option(variable)
            print(option)
            card = self._create_variable_card(
                text=option.title, component_id=option.id, input_type=option.type, value=default_values.get(option.title, None)
            )
            layout.append(card)
        return layout


class VariableSelectorOption:

    def __init__(self, variable_title, variable_type):
        self.title = variable_title
        self.id = f"var-{variable_title}"
        self.type = variable_type

        VariableSelector._variableselectoroptions.append(self)

    def is_valid(self):
        pass

    def __str__(self):
        return f"Title: {self.title}\nId: {self.id}\nType: {self.type}\n"


"""Here we define some default values that are available from the get-go"""
# Periods
VariableSelectorOption("aar", "number")
VariableSelectorOption("termin", "number")
VariableSelectorOption("måned", "number")
# Groupings
VariableSelectorOption("nace", "text")
VariableSelectorOption("fylke", "text")
VariableSelectorOption("nspekfelt", "text")
VariableSelectorOption("prodcomkode", "text")
# Identifiers
VariableSelectorOption("oppgavegiver", "text")
VariableSelectorOption("foretak", "text")
VariableSelectorOption("bedrift", "text")
VariableSelectorOption("skjemaenhet", "text")

VariableSelector._variableselectoroptions

print(VariableSelector._variableselectoroptions[0])

demo = VariableSelector(selected_inputs=["orgf"], selected_states=["aar", "nace"])

demo.states
