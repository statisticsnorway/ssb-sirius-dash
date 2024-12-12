import logging
from typing import Any
from typing import cast

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import html
from dash.exceptions import PreventUpdate

from ..control.framework import Kvalitetsrapport
from ..control.framework import lag_kontroll_dokumentasjon
from .modal_functions import sidebar_button

# +

logger = logging.getLogger(__name__)

ident_options = [
    {
        "orgb": ("var-bedrift", "value"),
        "orgf": ("var-foretak", "value"),
    }
]


class Kontroller:
    """Provides a layout and functionality for a modal that offers an overview of data checks and control results.

    Attributes:
        ident (str): Name of the identification variable, e.g., 'orgf'.
        kontroll_dokumentasjon_path (str): Path to the saved quality report in JSON format on Dapla.
    """

    def __init__(self, ident: str, kvalitetsrapport_path: str) -> None:
        """Initialize the Kontroller module.

        This method sets up the identification variable, loads the quality report from a JSON file,
        and prepares data tables for control documentation and outputs.

        Args:
            ident (str): The key for the identification variable, e.g., 'orgf'.
            kvalitetsrapport_path (str): Path to the quality report saved as a JSON file on Dapla.

        Attributes Set:
            ident (str): The resolved name of the identification variable.
            kontrolltabell (pd.DataFrame): A table documenting the performed controls.
            utslagstabell (pd.DataFrame): A table detailing the control outputs.
        """
        self.ident = ident_options[0][ident]
        if kvalitetsrapport_path:
            data = Kvalitetsrapport.from_json(kvalitetsrapport_path).to_dict()
            self.kontrolltabell = lag_kontroll_dokumentasjon(data)
            self.utslagstabell = pd.DataFrame(data["kontrollutslag"])
        self.callbacks()

    def layout(self) -> html.Div:
        """Generates the layout for the Kontroller modal.

        Returns:
            dash.html.Div: Layout containing the Kontroller modal and interactive components.
        """
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
        """Sets up interactivity for the Kontroller modal, including linking table clicks and navigation back to the main view."""

        @callback(  # type: ignore[misc]
            Output("kontroller-modal", "is_open"),
            Input("sidebar-kontroller-button", "n_clicks"),
            State("kontroller-modal", "is_open"),
        )
        def kontrollermodal_toggle(n: int | None, is_open: bool) -> bool:
            """Toggles the open/close state of the Kontroller modal.

            Args:
                n (int | None): Number of clicks on the sidebar button.
                is_open (bool): Current state of the modal.

            Returns:
                bool: Updated state of the modal.
            """
            if n:
                return not is_open
            return is_open

        @callback(  # type: ignore[misc]
            Output("kontroll-table-detailed", "filterModel"),
            Input("kontroll-table-overview", "cellClicked"),
            State("kontroll-table-overview", "rowData"),
        )
        def kontroll_main_click(
            click: dict[str, int | dict[str, Any] | None] | None,
            rowdata: list[dict[str, Any]],
        ) -> dict[str, dict[str, str]]:
            """Links clicks on the control overview table to filter the detailed control results table.

            Args:
                click (dict | None): Data about the clicked cell in the overview table.
                rowdata (dict): Data from the rows in the overview table.

            Returns:
                dict: Filter model to apply to the detailed results table.

            Raises:
                PreventUpdate: Stops the callback if click is None.
            """
            if not click or not isinstance(click.get("rowIndex"), int):
                raise PreventUpdate
            row_index = cast(int, click["rowIndex"])
            try:
                kontroll = rowdata[row_index]["kontroll_id"]
            except (IndexError, KeyError) as e:
                raise PreventUpdate from e
            return {
                "kontrollnavn": {
                    "filterType": "text",
                    "type": "contains",
                    "filter": kontroll,
                }
            }

        @callback(  # type: ignore[misc]
            Output(self.ident[0], self.ident[1]),
            Input("kontroll-table-detailed", "cellClicked"),
            State("kontroll-table-detailed", "rowData"),
        )
        def kontroll_detail_click(
            click: dict[str, int | dict[str, Any] | None] | None,
            rowdata: list[dict[str, Any]],
        ) -> str:
            """Links clicks in the detailed control results table to select the identification variable value.

            Args:
                click (dict | None): Data about the clicked cell in the detailed table.
                rowdata (dict): Data from the rows in the detailed table.

            Returns:
                str: Selected identification variable value.

            Raises:
                PreventUpdate: Stops the callback if click is None.
            """
            if not click or not isinstance(click.get("rowIndex"), int):
                raise PreventUpdate

            row_index = cast(int, click["rowIndex"])
            try:
                observation = rowdata[row_index]["observasjon_id"]
            except (IndexError, KeyError) as e:
                raise PreventUpdate from e

            if not isinstance(observation, str):
                logger.warning(
                    f"observation_id should be str, is {type(observation).__name__}"
                )
            return str(observation)
