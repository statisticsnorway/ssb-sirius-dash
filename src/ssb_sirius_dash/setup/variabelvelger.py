import dash_bootstrap_components as dbc
from dash import html

variable_options = {
    "aar": {"title": "År", "id": "var-aar", "type": "number"},
    "termin": {"title": "Termin", "id": "var-termin", "type": "number"},
    "nace": {"title": "Nace", "id": "var-nace", "type": "text"},
    "oppgavegiver": {"title": "Oppgavegiver", "id": "var-oppgavegiver", "type": "text"},
    "foretak": {"title": "Foretak", "id": "var-foretak", "type": "text"},
    "bedrift": {"title": "Bedrift", "id": "var-bedrift", "type": "text"},
    "fylke": {"title": "Fylke", "id": "var-fylke", "type": "text"},
    "skjemaenhet": {"title": "Skjemaenhet", "id": "var-skjemaenhet", "type": "text"},
    "prodcomkode": {"title": "Prodcomkode", "id": "var-prodcomkode", "type": "text"},
    "nspekfelt": {"title": "NSPEK-felt", "id": "var-nspekfelt", "type": "text"},
}


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


def generate_skjermcards(selected_keys, default_values=None):
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
