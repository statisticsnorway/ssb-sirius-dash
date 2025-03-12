import logging
from typing import Any

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from ..setup.variableselector import VariableSelector
from ..utils.functions import sidebar_button

logger = logging.getLogger(__name__)


class PivotTable:
    """

    Data should have grouping values (kommunenr) as columns
    """
    def __init__(self, get_data, states):
        self.get_data = get_data
        self.variableselector = VariableSelector(selected_inputs=[],selected_states=states)
        self.dropdown_options = [{"label": x, "value": x} for x in self.variableselector.selected_variables]
        self.callbacks()

    def layout(self):
        layout = html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader([dbc.ModalTitle("📋 Pivot table")]),
                        dbc.ModalBody(
                            [
                                dbc.Row([dcc.Dropdown(id = "pivot-dropdown-index", options = self.dropdown_options), dcc.Dropdown(id = "pivot-dropdown-columns", options = self.dropdown_options), dbc.Button("KJØR", id="pivot-run-button")]),
                                dbc.Row(
                                    dag.AgGrid(
                                        id="pivot-table-overview",
                                    ),
                                )
                            ]
                        ),
                    ],
                    id="pivot-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button("📋", "Pivot table", "sidebar-pivot-button"),
            ]
        )
        return layout

    def callbacks(self):
        dynamic_states = self.variableselector.get_states()

        @callback(  # type: ignore[misc]
            Output("pivot-modal", "is_open"),
            Input("sidebar-pivot-button", "n_clicks"),
            State("pivot-modal", "is_open"),
        )
        def pivotmodal_toggle(n: int | None, is_open: bool) -> bool:
            """Toggles the open/close state of the control modal.

            Args:
                n (int | None): Number of clicks on the sidebar button.
                is_open (bool): Current state of the modal.

            Returns:
                bool: Updated state of the modal.
            """
            if n:
                return not is_open
            return is_open
        
        @callback(
            Output("pivot-table-overview", "rowData"),
            Output("pivot-table-overview", "columnDefs"),
            Input("pivot-run-button", "n_clicks"),
            State("pivot-dropdown-index", "value"),
            State("pivot-dropdown-columns", "value"),
            
        )
        def load_data(click, index, columns):
            if click:
                if not isinstance(index, list):
                    index = [index]
                if not isinstance(columns, list):
                    columns = [columns]
                df = self.get_data()
                return df.pivot_table(index=index, columns=columns, values = "value", aggfunc="sum").reset_index().to_dict("records"), columndefs

