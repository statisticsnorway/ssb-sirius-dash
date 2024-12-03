import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html
from dash.development.base_component import Component

from ..control.framework import Kvalitetsrapport
from ..control.framework import lag_kontroll_dokumentasjon
from .modal_functions import sidebar_button

# +
ident_options = [
    {
        "orgb": ("var-bedrift", "value"),
        "orgf": ("var-foretak", "value"),
    }
]


class Kontroller:
    """Class for å inkludere et skjermbilde som viser oversikt over kontroller som er gjort på dataene og kontrollutslag.

    Attributes:
    -----------
    ident : str
        Variabelnavn på identifikasjonsvariabelen. F.eks. orgf
    kontroll_dokumentasjon_path : str
        Filsti til lagret kvalitetsrapport i json.format på Dapla.
    """

    def __init__(self, ident: str, kvalitetsrapport_path: str) -> None:
        """Setter opp modulen med callbacks og nødvendig informasjon fra kvalitetsrapport til å vise kontroller og kontrollutslag."""
        self.ident = ident_options[0][ident]
        if kvalitetsrapport_path:
            data = Kvalitetsrapport.from_json(kvalitetsrapport_path).to_dict()
            self.kontrolltabell = lag_kontroll_dokumentasjon(data)
            self.utslagstabell = pd.DataFrame(data["kontrollutslag"])
        self.callbacks()

    def layout(self) -> Component:
        """Lager layouten til Kontroller modalen."""
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader([dbc.ModalTitle("⚠️ Kontroller")]),
                        dbc.ModalBody(
                            [
                                dag.AgGrid(
                                    id="kontroll-table-overview",
                                    columnDefs=[
                                        {"field": x}
                                        for x in [
                                            "kontroll_id",
                                            "kontrolltype",
                                            "feilbeskrivelse",
                                            "Enheter i datasettet",
                                            "Enheter kontrollert",
                                            "Kontrollutslag",
                                        ]
                                    ],
                                    rowData=self.kontrolltabell.to_dict(
                                        orient="records"
                                    ),
                                ),
                                dag.AgGrid(
                                    id="kontroll-table-detailed",
                                    columnDefs=[
                                        {"field": x}
                                        for x in ["observasjon_id", "feilbeskrivelse"]
                                    ]
                                    + [
                                        {
                                            "field": "kontrollnavn",
                                            "hide": True,
                                            "filter": True,
                                        }
                                    ],
                                    rowData=self.utslagstabell.to_dict(
                                        orient="records"
                                    ),
                                ),
                            ]
                        ),
                    ],
                    id="kontroller-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button("⚠️", "Kontroller", "sidebar-kontroller-button"),
            ]
        )

    def callbacks(self) -> None:
        """Funksjon som brukes av class-en for å sette opp klikkbarhet mellom tabellene og tilbake til hovedvisningen."""

        @callback(
            Output("kontroller-modal", "is_open"),
            Input("sidebar-kontroller-button", "n_clicks"),
            State("kontroller-modal", "is_open"),
        )
        def kontrollermodal_toggle(n: int | None, is_open: bool) -> bool:
            """Åpner og lukker modalen."""
            if n:
                return not is_open
            return is_open

        @callback(
            Output("kontroll-table-detailed", "filterModel"),
            Input("kontroll-table-overview", "cellClicked"),
            State("kontroll-table-overview", "rowData"),
        )
        def kontroll_main_click(click: dict | None, rowData: dict) -> dict:
            """Kobler klikk fra tabell med oversikt over kontrollene mot filtrering av kontrollutslagtabellen."""
            if click:
                kontroll = rowData[click["rowIndex"]]["kontroll_id"]
                return {
                    "kontrollnavn": {
                        "filterType": "text",
                        "type": "contains",
                        "filter": kontroll,
                    }
                }

        @callback(
            Output(self.ident[0], self.ident[1]),
            Input("kontroll-table-detailed", "cellClicked"),
            State("kontroll-table-detailed", "rowData"),
        )
        def kontroll_detail_click(click: dict | None, rowData: dict) -> str:
            """Kobler klikk fra kontrollutslagtabell til valgt ident variabel fra variabelvelgeren."""
            if click:
                return rowData[click["rowIndex"]]["observasjon_id"]
