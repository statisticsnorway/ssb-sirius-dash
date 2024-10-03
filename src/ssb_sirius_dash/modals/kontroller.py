import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html

from ssb_sirius_dash import sidebar_button

from ..control.framework import Kvalitetsrapport
from ..control.framework import lag_kontroll_dokumentasjon

# +
ident_options = [
    {
        "orgb": ("var-bedrift", "value"),
        "orgf": ("var-foretak", "value"),
    }
]


class Kontroller:
    def __init__(self, ident, kvalitetsrapport_path):
        self.ident = ident_options[0][ident]
        if kvalitetsrapport_path:
            data = Kvalitetsrapport.from_json(kvalitetsrapport_path).to_dict()
            self.kontrolltabell = lag_kontroll_dokumentasjon(data)
            self.utslagstabell = pd.DataFrame(data["kontrollutslag"])
        self.callbacks()

    def layout(self):
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

    def callbacks(self):
        @callback(
            Output("kontroller-modal", "is_open"),
            Input("sidebar-kontroller-button", "n_clicks"),
            State("kontroller-modal", "is_open"),
        )
        def kontrollermodal_toggle(n, is_open):
            if n:
                return not is_open
            return is_open

        @callback(
            Output("kontroll-table-detailed", "filterModel"),
            Input("kontroll-table-overview", "cellClicked"),
            State("kontroll-table-overview", "rowData"),
        )
        def kontroll_main_click(click, rowData):
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
        def kontroll_detail_click(click, rowData):
            if click:
                return rowData[click["rowIndex"]]["observasjon_id"]
