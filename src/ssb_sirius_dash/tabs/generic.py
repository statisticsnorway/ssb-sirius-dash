import datetime

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import callback
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

input_options = {
    "orgb": Input("var-bedrift", "value"),
    "orgf": Input("var-foretak", "value"),
    "oppgavegiver": Input("var-oppgavegiver", "value"),
    "skjemaident": Input("var-skjemaident", "value"),
}

states_options = [
    {
        "aar": ("var-aar", "value"),
        "maaned": {"var-maaned", "value"},
        "termin": ("var-termin", "value"),
        "nace": ("var-nace", "value"),
    }
]


class EditingTable:
    """A component for editing database tables using a Dash AgGrid table.

    This class provides a layout and functionality to:
    - Select a database table from a dropdown menu.
    - Load data into an editable Dash AgGrid table.
    - Update database values based on user edits in the table.

    Attributes:
    -----------
    label : str
        The label for the tab or component.
    database : object
        Database connection or interface for querying and updating data.
    tables : list of str
        List of available table names for selection.
    var_input : str
        Variable input key for identifying records in the database.
    states : list of str
        Keys representing dynamic states to filter data.
    get_data : callable
        Function to fetch data from the database.
    update_table : callable
        Function to update database records based on edits in the table.
    dropdown_options : list of dict
        List of options for the dropdown menu, derived from `tables`.

    Methods:
    --------
    layout()
        Generates the layout for the table editing component.
    callbacks()
        Registers the Dash callbacks for loading and updating table data.
    """

    def __init__(
        self,
        label: str,
        database: object,
        tables: list,
        var_input: str,
        states: list,
        get_data_func: callable,
        update_table_func: callable,
    ) -> None:
        """Initialize the EditingTable component.

        Parameters
        ----------
        label : str
            Label for the tab or component.
        database : object
            Database connection or interface used for querying and updating data.
        tables : list of str
            List of available table names for selection.
        var_input : str
            Variable input key used to identify records (e.g., "orgb", "orgf").
        states : list of str
            Keys representing dynamic states to filter data (e.g., "aar", "termin").
        get_data_func : callable
            Function for retrieving data from the database.
        update_table_func : callable
            Function for updating data in the database.

        Attributes:
        -----------
        label : str
            The label for the component.
        database : object
            Database connection or interface.
        dropdown_options : list of dict
            Options for the dropdown menu, created from `tables`.
        selected_ident : dash.dependencies.Input
            Input dependency for the selected variable.
        states : list of str
            List of dynamic states for filtering data.
        get_data : callable
            Function to fetch data from the database.
        update_table : callable
            Function to update data in the database.
        """
        dropdown_options = [{"label": table, "value": table} for table in tables]

        self.selected_ident = input_options[var_input]
        self.states = states
        self.get_data = get_data_func
        self.update_table = update_table_func
        self.database = database
        self.dropdown_options = dropdown_options
        self.callbacks()
        self.label = label

    def layout(self) -> html.Div:
        """Generate the layout for the EditingTable component.

        Returns:
        --------
        A Div element containing:
        - A dropdown menu to select a database table.
        - An editable Dash AgGrid table for displaying and modifying data.
        - A status message for updates.
        """
        layout = html.Div(
            style={"height": "100vh", "display": "flex", "flexDirection": "column"},
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="tab-tabelleditering-dd1",
                            options=self.dropdown_options,
                            value=self.dropdown_options[0]["value"],
                            placeholder="Velg tabell",
                            className="dbc",
                        ),
                        dag.AgGrid(
                            defaultColDef={"editable": True},
                            id="tab-tabelleditering-table1",
                            className="ag-theme-alpine-dark header-style-on-filter",
                        ),
                        html.P(id="tab-tabelleditering-status1"),
                    ],
                ),
            ],
        )
        return layout

    def callbacks(self) -> None:
        """Register Dash callbacks for the EditingTable component.

        Notes:
        ------
        - The `load_ag_grid` callback loads data into the table based on the selected table
          and filter states.
        - The `update_table` callback updates database values when a cell value is changed.
        """
        states_dict = states_options[0]
        dynamic_states = [
            State(states_dict[key][0], states_dict[key][1]) for key in self.states
        ]

        @callback(
            Output("tab-tabelleditering-table1", "rowData"),
            Output("tab-tabelleditering-table1", "columnDefs"),
            Input("tab-tabelleditering-dd1", "value"),
            self.selected_ident,
            *dynamic_states,
        )
        def load_ag_grid(tabell: str, ident: str, *dynamic_states: list) -> tuple:
            """Load data into the Dash AgGrid table.

            Parameters
            ----------
            tabell : str
                Name of the selected database table.
            ident : str
                Identifier for filtering records (e.g., "var-bedrift").
            dynamic_states : list
                Dynamic state parameters for filtering data.

            Returns:
            --------
            A tuple containing:
            - rowData (list of dict): Records to display in the table.
            - columnDefs (list of dict): Column definitions for the table.

            Notes:
            ------
            - Columns are dynamically generated based on the table's schema.
            - The "row_id" column is hidden by default but used for updates.
            - Adds checkbox selection to the first column for bulk actions.
            """
            try:
                states_values = dynamic_states[: len(self.states)]
                state_params = {
                    key: value
                    for key, value in zip(self.states, states_values, strict=False)
                }

                args = []
                for key in self.states:
                    var = state_params.get(key)
                    if var is not None:
                        args.append(var)
                if "nace" in state_params and state_params["nace"] is not None:
                    n = len(state_params["nace"])
                    args.append(n)
                df = self.get_data(self.database, ident, tabell, *args)
                columns = [
                    {
                        "headerName": col,
                        "field": col,
                        "hide": True if col == "row_id" else False,
                    }
                    for col in df.columns
                ]
                columns[0]["checkboxSelection"] = True
                columns[0]["headerCheckboxSelection"] = True
                return df.to_dict("records"), columns
            except Exception as e:
                raise e

        @callback(
            Output("error_log", "children", allow_duplicate=True),
            Input("tab-tabelleditering-table1", "cellValueChanged"),
            State("tab-tabelleditering-dd1", "value"),
            State("error_log", "children"),
            *dynamic_states,
            prevent_initial_call=True,
        )
        def update_table(
            edited: list, tabell: str, error_log: list, *dynamic_states: list
        ) -> dbc.Alert:
            """Update the database based on edits made in the AgGrid table.

            Parameters
            ----------
            edited : list of dict
                Information about the edited cell, including:
                - colId: The column name of the edited cell.
                - oldValue: The previous value of the cell.
                - value: The new value of the cell.
                - data: The row data, including the "row_id".
            tabell : str
                The name of the table being edited.
            dynamic_states : list
                Dynamic state parameters for filtering data.

            Returns:
            --------
            A status message indicating the success or failure of the update.

            Notes:
            ------
            - The function calls `update_table` to apply the change to the database.
            - If the update succeeds, a confirmation message is returned.
            - If the update fails, an error message is displayed.
            """
            if not edited:
                raise PreventUpdate
            states_values = dynamic_states[: len(self.states)]
            state_params = {
                key: value
                for key, value in zip(self.states, states_values, strict=False)
            }

            args = []
            for key in self.states:
                var = state_params.get(key)
                if var is not None:
                    args.append(var)
            variable = edited[0]["colId"]
            old_value = edited[0]["oldValue"]
            new_value = edited[0]["value"]
            row_id = edited[0]["data"]["row_id"]
            try:
                self.update_table(
                    self.database, variable, new_value, row_id, tabell, *args
                )

                new_alert = dbc.Alert(
                    f"{datetime.datetime.now()} - {variable} updatert fra {old_value} til {new_value}",
                    color="info",
                    dismissable=True,
                )

                return [new_alert, *error_log]

            except Exception:
                new_alert = dbc.Alert(
                    f"{datetime.datetime.now()} - Oppdatering av {variable} fra {old_value} til {new_value} feilet!",
                    color="danger",
                    dismissable=True,
                )
                return [new_alert, *error_log]
