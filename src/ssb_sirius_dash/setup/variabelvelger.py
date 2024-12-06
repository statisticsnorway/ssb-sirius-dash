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


def skjermcard(
    text: str, component_id: str, input_type: str, value: str | None = None
) -> dbc.Col:
    """Generate a Dash Bootstrap card with an input field.

    Parameters
    ----------
    text : str
        The title text to display on the card.
    component_id : str
        The ID to assign to the input field within the card.
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


def generate_skjermcards(
    selected_keys: list, default_values: dict | None = None
) -> list:
    """Generate a list of Dash Bootstrap cards based on selected variable keys.

    Parameters
    ----------
    selected_keys : list of str
        Keys representing variables to include as cards. Each key corresponds
        to an entry in the `variable_options` dictionary.
    default_values : dict, optional
        A dictionary containing default values for the cards, where the keys
        are variable names, and the values are the default input values. Defaults to an empty dictionary.

    Returns:
    --------
    list of dash_bootstrap_components.Col
        A list of cards, each represented as a Dash Bootstrap column.
    """
    if default_values is None:
        default_values = {}
    cards_list = []
    for key in selected_keys:
        card_config = variable_options.get(key, {})
        title = card_config.get("title")
        card_id = card_config.get("id")
        card_type = card_config.get("type")
        value = default_values.get(key, None)

        card = skjermcard(title, card_id, card_type, value)
        cards_list.append(card)
    return cards_list
