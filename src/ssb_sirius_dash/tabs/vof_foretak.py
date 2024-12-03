import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import duckdb
import pyarrow.parquet as pq
from dapla import FileClient
from dash import callback
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

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
    "f_kommunenr",
]


class VoFForetakTab:
    """Tab for displaying and managing information from VoF.

    This component:
    - Displays detailed information about selected foretak using cards.
    - Provides a table for associated business data.
    - Interacts with a DuckDB in-memory database to fetch data.

    Attributes:
    -----------
    database : duckdb.DuckDBPyConnection
        In-memory database connection for querying VoF foretak data.
    label : str
        Label for the tab, displayed as "🗃️ VoF Foretak".

    Methods:
    --------
    generate_card(title, component_id, var_type)
        Generates a Dash Bootstrap card for displaying information.
    register_table()
        Registers the VoF foretak data as a table in DuckDB.
    layout()
        Generates the layout for the VoF Foretak tab.
    callbacks()
        Registers Dash callbacks for handling user interactions.
    """

    def __init__(self) -> None:
        """Initialize the VoFForetakTab component.

        Attributes:
        -----------
        database : duckdb.DuckDBPyConnection
            In-memory database connection for querying VoF foretak data.
        label : str
            The label for the tab, displayed as "🗃️ VoF Foretak".
        """
        self.database = self.register_table()
        self.callbacks()
        self.label = "🗃️ VoF Foretak"

    def generate_card(self, title: str, component_id: str, var_type: str) -> dbc.Card:
        """Generate a Dash Bootstrap card for displaying data.

        Parameters
        ----------
        title : str
            Title displayed in the card header.
        component_id : str
            ID assigned to the input component inside the card.
        var_type : str
            Input type for the component (e.g., "text").

        Returns:
        --------
        dash_bootstrap_components.Card
            A styled card containing an input field.
        """
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

    def register_table(self) -> duckdb.DuckDBPyConnection:
        """Register the VoF foretak data as a DuckDB table.

        Returns:
        --------
        A connection to an in-memory DuckDB instance with the VoF foretak data registered.
        """
        fs = FileClient.get_gcs_file_system()
        fil_ssb_foretak = "ssb-vof-data-delt-oracle-prod/vof-oracle_data/klargjorte-data/ssb_foretak.parquet"
        ssb_foretak = pq.read_table(fil_ssb_foretak, columns=VOF_COLUMNS, filesystem=fs)
        dsbbase = duckdb.connect()
        dsbbase.register("ssb_foretak", ssb_foretak)
        return dsbbase

    def layout(self) -> html.Div:
        """Generate the layout for the VoF Foretak tab.

        Returns:
        --------
        A Div element containing:
        - Cards displaying detailed information about foretak.
        """
        layout = html.Div(
            style={"height": "100%", "display": "flex", "flexDirection": "column"},
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
                                self.generate_card(
                                    "Orgnr", "tab-vof_foretak-orgnrcard", "text"
                                ),
                                self.generate_card(
                                    "Navn", "tab-vof_foretak-navncard", "text"
                                ),
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
                                self.generate_card(
                                    "Nace", "tab-vof_foretak-nacecard", "text"
                                ),
                                self.generate_card(
                                    "Statuskode", "tab-vof_foretak-statuscard", "text"
                                ),
                                self.generate_card(
                                    "Ansatte", "tab-vof_foretak-ansattecard", "text"
                                ),
                                self.generate_card(
                                    "Sektor 2014", "tab-vof_foretak-sektorcard", "text"
                                ),
                                self.generate_card(
                                    "Kommunenummer",
                                    "tab-vof_foretak-kommunecard",
                                    "text",
                                ),
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
                                self.generate_card(
                                    "Organisasjonsform",
                                    "tab-vof_foretak-orgformcard",
                                    "text",
                                ),
                                self.generate_card(
                                    "Størrelseskode",
                                    "tab-vof_foretak-størrelsecard",
                                    "text",
                                ),
                                self.generate_card(
                                    "Ansatte tot.",
                                    "tab-vof_foretak-totansattecard",
                                    "text",
                                ),
                                self.generate_card(
                                    "Undersektor",
                                    "tab-vof_foretak-undersektorcard",
                                    "text",
                                ),
                                self.generate_card(
                                    "Type", "tab-vof_foretak-typecard", "text"
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Tilhørende virksomheter",
                                    style={
                                        "textAlign": "center",
                                        "fontWeight": "bold",
                                    },
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

    def callbacks(self) -> None:
        """Register Dash callbacks for the VoF Foretak tab.

        Notes:
        ------
        - The `vof_data` callback fetches and updates data in the cards based on the selected foretak.
        """

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
            State("var-aar", "value"),  # Is not used in this iteration
        )
        def vof_data(orgf: str, aar: int) -> tuple:
            """Fetch VoF Foretak data based on the selected organization number.

            Parameters
            ----------
            orgf : str
                The organization number of the selected foretak.
            aar : int
                The year for filtering data (if applicable).

            Returns:
            --------
            tuple
                A tuple containing information about the foretak

            Notes:
            ------
            - If `orgf` is None, no data is returned.
            - The callback queries the DuckDB database for the selected organization number.
            """
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
                return (
                    orgnr,
                    navn,
                    nace,
                    statuskode,
                    ansatte,
                    sektor,
                    kommune,
                    orgform,
                    størrelse,
                    ansatte_tot,
                    undersektor,
                    typen,
                )
