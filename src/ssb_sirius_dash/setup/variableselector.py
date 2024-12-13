import dash_bootstrap_components as dbc
from dash import html

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
    return card


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
