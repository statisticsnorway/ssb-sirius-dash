import base64

import dash_bootstrap_components as dbc
from dapla import FileClient
from dash import callback
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.exceptions import PreventUpdate


class AarsregnskapTab:
    """Tab for displaying annual financial statements (Årsregnskap).

    Attributes:
    -----------
    label : str
        Label for the tab, displayed as "🧾 Årsregnskap".
    """

    def __init__(
        self,
    ) -> None:
        """Initialize the AarsregnskapTab component.

        Attributes:
        -----------
        label : str
            Label for the tab, displayed as "🧾 Årsregnskap".
        """
        self.label = "🧾 Årsregnskap"
        self.callbacks()

    def layout(self) -> html.Div:
        """Generate the layout for the Årsregnskap tab.

        Returns:
        --------
        A Div element containing input fields for year and organization number
        and an iframe to display the PDF content.
        """
        layout = html.Div(
            style={"height": "100%", "display": "flex", "flexDirection": "column"},
            children=[
                dbc.Container(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Label("År"),
                                            dbc.Input(
                                                "tab-aarsregnskap-input1", type="number"
                                            ),
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
                        html.Iframe(
                            id="tab-aarsregnskap-iframe1",
                            style={"width": "100%", "height": "80vh"},
                        ),
                    ],
                    fluid=True,
                ),
            ],
        )
        return layout

    def callbacks(self) -> None:
        """Register Dash callbacks for the Årsregnskap tab."""

        @callback(
            Output("tab-aarsregnskap-input1", "value"),
            Input("var-aar", "value"),
        )
        def update_aar(aar: int):
            """Update the year input field based on the selected year.

            Parameters
            ----------
            aar : int
                The selected year.

            Returns:
            --------
            The updated year value.
            """
            return aar

        @callback(
            Output("tab-aarsregnskap-input2", "value"),
            Input("var-foretak", "value"),
        )
        def update_orgnr(orgnr: str):
            """Update the organization number input field.

            Parameters
            ----------
            orgnr : str
                The selected organization number.

            Returns:
            --------
            str
                The updated organization number value.
            """
            return orgnr

        @callback(
            Output("tab-aarsregnskap-iframe1", "src"),
            Input("tab-aarsregnskap-input1", "value"),
            Input("tab-aarsregnskap-input2", "value"),
        )
        def update_pdf_source(aar: int, orgnr: str):
            """Fetch and encode the PDF source based on the year and organization number.

            Parameters
            ----------
            aar : int
                The year input value.
            orgnr : str
                The organization number input value.

            Returns:
            --------
            str
                A data URI for the PDF file, encoded in base64.

            Raises:
            ------
            dash.exceptions.PreventUpdate
                If the year or organization number is not provided.
            """
            if not aar or not orgnr:
                raise PreventUpdate
            try:
                fs = FileClient.get_gcs_file_system()
                with fs.open(
                    f"gs://ssb-skatt-naering-data-produkt-prod/aarsregn/g{aar}/{orgnr}_{aar}.pdf",
                    "rb",
                ) as f:
                    pdf_bytes = f.read()

                pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
                pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"
            except FileNotFoundError:
                return None
            pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"
            return pdf_data_uri
