import os
from flask import Flask, Response, request
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from google.cloud import storage
from dapla import FileClient
import base64


class AarsregnskapTab:
    def __init__(
        self,
    ):
        self.label = "🧾 Årsregnskap"
        self.callbacks()

    def layout(self):
        layout = html.Div(
            style = {
                "height": "100%",
                "display": "flex",
                "flexDirection": "column"
            },
            children=[
                dbc.Container(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                        dbc.Label("År"),
                                        dbc.Input("tab-aarsregnskap-input1", type="number"),
                                        ]
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                        dbc.Label("Orgnr"),
                                        dbc.Input("tab-aarsregnskap-input2"),
                                        ]
                                    )
                                ),
                            ]
                        ),
                        html.Iframe(id="tab-aarsregnskap-iframe1", style={"width": "100%", "height": "80vh"})
                    ],
                    fluid=True,
                ),
            ],
        )
        return layout

    def callbacks(self):
        @callback(
            Output("tab-aarsregnskap-input1", "value"),
            Input("var-aar", "value"),
        )
        def update_aar(aar):
            return aar

        @callback(
            Output("tab-aarsregnskap-input2", "value"),
            Input("var-foretak", "value"),
        )
        def update_orgnr(orgnr):
            return orgnr
 
        @callback(
            Output("tab-aarsregnskap-iframe1", "src"),
            Input("tab-aarsregnskap-input1", "value"),
            Input("tab-aarsregnskap-input2", "value")
        )
        def update_pdf_source(aar, orgnr):
            if not aar or not orgnr:
                raise PreventUpdate
            try:
                fs = FileClient.get_gcs_file_system()
                with fs.open(f"gs://ssb-skatt-naering-data-produkt-prod/aarsregn/g{aar}/{orgnr}_{aar}.pdf", "rb") as f:
                    pdf_bytes = f.read()

                pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
                pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"
            except FileNotFoundError:
                return None
            pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"
            return pdf_data_uri
