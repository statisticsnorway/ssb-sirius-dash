import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import callback, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import ast

class FrisøkTab:
    def __init__(self, database):
        self.database = database
        self.label = "🔍 Frisøk"

    def layout(self):
        layout = html.Div(
            [
                html.Div(
                    dbc.Textarea(
                        id="tab-frisøk-textarea1", size="xxl",
                        placeholder="SELECT * FROM databasetabell",

                    ),
                ),
                html.Div(
                    style={
                        "display": "grid",
                        "grid-template-columns": "80% 20%"
                    },
                    children = [
                        dbc.Input(
                            id="tab-frisøk-input1",
                            placeholder="Velg partisjoner. f.eks. {'aar': [2023], 'termin':[1, 2]}",
                        ),
                        dbc.Button(
                            "kjør",
                            id="tab-frisøk-button1",
                        ),
                    ]
                ),
                dag.AgGrid(
                    defaultColDef={"editable": True},
                    id="tab-frisøk-table1",
                    className="ag-theme-alpine-dark header-style-on-filter",
                )
            ]
        )
        return layout

    def callbacks(self):
        @callback(
            Output("tab-frisøk-table1", "rowData"),
            Output("tab-frisøk-table1", "columnDefs"),
            Input("tab-frisøk-button1", "n_clicks"),
            State("tab-frisøk-textarea1", "value"),
            State("tab-frisøk-input1", "value"),
        )
        def table_frisøk(n_clicks, query, partisjoner):
            if n_clicks > 0:
                if partisjoner is not None:
                    partisjoner = ast.literal_eval(partisjoner)
                df = self.database.query(query, partition_select=partisjoner)
                columns = [{"headerName": col, "field": col, "hide": True if col == "row_id" else False} for col in df.columns]
                return df.to_dict("records"), columns