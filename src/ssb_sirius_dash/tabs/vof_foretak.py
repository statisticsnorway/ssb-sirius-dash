import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pyarrow.parquet as pq
import duckdb
from dapla import FileClient

VOF_COLUMNS = [
    "orgnr",
    "navn",
    "sn07_1",
    "org_form",
    "statuskode",
    "antall_ansatte",
    "ansatte_totalt",
    "sektor_2014",
    "undersektor_2014",
    "sf_type",
    "f_kommunenr"
]

class VoFForetakTab:
    def __init__(self):
        self.database = self.register_table()
        self.callbacks()
        self.label = "🗃️ VoF Foretak"

    def generate_card(self, title, component_id, var_type):
        card = dbc.Card(
            [
                dbc.CardHeader(title),
                dbc.CardBody(
                    [
                        dbc.Input(id=component_id, type=var_type),
                    ],
                    style={"overflowY": "auto"},
                ),
            ],
            style={"height": "100%", "display": "flex", "flexDirection": "column"},
        )
        return card

    def register_table(self):
        fs = FileClient.get_gcs_file_system()
        fil_ssb_foretak = "ssb-vof-data-delt-prod/vof-oracle_data/klargjorte-data/ssb_foretak.parquet"
        ssb_foretak = pq.read_table(
            fil_ssb_foretak,
            columns=VOF_COLUMNS,
            filesystem = fs
        )
        dsbbase = duckdb.connect()
        dsbbase.register("ssb_foretak", ssb_foretak)
        return dsbbase

    def layout(self):
        layout = html.Div(
            style = {
                "height": "100%",
                "display": "flex",
                "flexDirection": "column"
            },
            children=[
                html.Div(
                    style={
                        "height": "100%",
                        "overflow": "hidden",
                        "display": "grid",
                        "grid-template-rows": "15% 15% 15% 5% 50%",
                    },
                    children=[
                        html.Div(
                            style={
                                "height": "100v%",
                                "overflow": "hidden",
                                "display": "grid",
                                "grid-template-columns": "20% 80%",
                            },
                            children=[
                                self.generate_card("Orgnr", "tab-vof_foretak-orgnrcard", "text"),
                                self.generate_card("Navn", "tab-vof_foretak-navncard", "text"),
                            ]
                        ),
                        html.Div(
                            style={
                                "height": "100%",
                                "overflow": "hidden",
                                "display": "grid",
                                "grid-template-columns": "20% 20% 20% 20% 20%",
                            },
                            children=[
                                self.generate_card("Nace", "tab-vof_foretak-nacecard", "text"),
                                self.generate_card("Statuskode", "tab-vof_foretak-statuscard", "text"),
                                self.generate_card("Ansatte", "tab-vof_foretak-ansattecard", "text"),
                                self.generate_card("Sektor 2014", "tab-vof_foretak-sektorcard", "text"),
                                self.generate_card("Kommunenummer", "tab-vof_foretak-kommunecard", "text"),
                            ],
                        ),
                        html.Div(
                            style={
                                "height": "100%",
                                "overflow": "hidden",
                                "display": "grid",
                                "grid-template-columns": "20% 20% 20% 20% 20%",
                            },
                            children=[
                                self.generate_card("Organisasjonsform", "tab-vof_foretak-orgformcard", "text"),
                                self.generate_card("Størrelseskode", "tab-vof_foretak-størrelsecard", "text"),
                                self.generate_card("Ansatte tot.", "tab-vof_foretak-totansattecard", "text"),
                                self.generate_card("Undersektor", "tab-vof_foretak-undersektorcard", "text"),
                                self.generate_card("Type", "tab-vof_foretak-typecard", "text"),
                            ],
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Tilhørende virksomheter",
                                    style={
                                        "textAlign": "center",
                                        "fontWeight": "bold",
                                    }
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dag.AgGrid(
                                    defaultColDef={"editable": True},
                                    id="tab-vof_foretak-table1",
                                    className="ag-theme-alpine-dark header-style-on-filter",
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        )
        return layout

    def callbacks(self):
        @callback(
            Output("tab-vof_foretak-orgnrcard", "value"),
            Output("tab-vof_foretak-navncard", "value"),
            Output("tab-vof_foretak-nacecard", "value"),
            Output("tab-vof_foretak-statuscard", "value"),
            Output("tab-vof_foretak-ansattecard", "value"),
            Output("tab-vof_foretak-sektorcard", "value"),
            Output("tab-vof_foretak-kommunecard", "value"),
            Output("tab-vof_foretak-orgformcard", "value"),
            Output("tab-vof_foretak-størrelsecard", "value"),
            Output("tab-vof_foretak-totansattecard", "value"),
            Output("tab-vof_foretak-undersektorcard", "value"),
            Output("tab-vof_foretak-typecard", "value"),
            Input("var-foretak", "value"),
            State("var-aar", "value"),
        )
        def vof_data(orgf, aar):
            if orgf is not None:
                df = self.database.execute(
                    f"SELECT * FROM ssb_foretak WHERE orgnr = '{orgf}'",
                ).df()

                df["ansatte_totalt"] = df["ansatte_totalt"].fillna(0)

                orgnr = df["orgnr"][0]
                navn = df["navn"][0]
                nace = df["sn07_1"][0]
                statuskode = df["statuskode"][0]
                ansatte = df["antall_ansatte"][0]
                sektor = df["sektor_2014"][0]
                kommune = df["f_kommunenr"][0]
                orgform = df["org_form"][0]
                størrelse = "S (placeholder)"
                ansatte_tot = df["ansatte_totalt"][0]
                undersektor = df["undersektor_2014"][0]
                typen = df["sf_type"][0]
                return orgnr, navn, nace, statuskode, ansatte, sektor, kommune, orgform, størrelse, ansatte_tot, undersektor, typen
