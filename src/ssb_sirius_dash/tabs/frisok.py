import ast

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import callback
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State


class FrisøkTab:
    """Tab for free-text SQL queries and displaying results in an AgGrid table.

    This class provides a layout for a tab that allows users to:
    - Enter SQL queries in a text area.
    - Optionally specify partition filters as a dictionary string.
    - Display the query results in an editable Dash AgGrid table.

    Attributes:
    -----------
    database : object
        Database connection or interface for executing SQL queries.
    label : str
        Label for the tab, displayed in the application.

    Methods:
    --------
    layout()
        Generates the layout for the tab.
    callbacks()
        Registers the Dash callbacks for interactivity.
    """

    def __init__(self, database: object) -> None:
        """Initialize the FrisøkTab with a database connection.

        Parameters
        ----------
        database : object
            Database connection or interface used for executing SQL queries.

        Attributes:
        -----------
        database : object
            The provided database connection or interface.
        label : str
            Label for the tab, set to "🔍 Frisøk".
        """
        self.database = database
        self.callbacks()
        self.label = "🔍 Frisøk"

    def layout(self) -> html.Div:
        """Generate the layout for the FrisøkTab.

        Returns:
        --------
        A Div element containing the text area for SQL queries, input for partitions,
        a button to run the query, and a Dash AgGrid table for displaying results.
        """
        layout = html.Div(
            [
                html.Div(
                    dbc.Textarea(
                        id="tab-frisøk-textarea1",
                        size="xxl",
                        placeholder="SELECT * FROM databasetabell",
                    ),
                ),
                html.Div(
                    style={"display": "grid", "grid-template-columns": "80% 20%"},
                    children=[
                        dbc.Input(
                            id="tab-frisøk-input1",
                            placeholder="Velg partisjoner. f.eks. {'aar': [2023], 'termin':[1, 2]}",
                        ),
                        dbc.Button(
                            "kjør",
                            id="tab-frisøk-button1",
                        ),
                    ],
                ),
                dag.AgGrid(
                    defaultColDef={"editable": True},
                    id="tab-frisøk-table1",
                    className="ag-theme-alpine-dark header-style-on-filter",
                ),
            ]
        )
        return layout

    def callbacks(self) -> None:
        """Register the Dash callbacks for the FrisøkTab.

        Notes:
        ------
        - This method registers a callback for executing the SQL query when the "kjør" button is clicked.
        - The results are displayed in the AgGrid table, with appropriate column definitions.
        """

        @callback(
            Output("tab-frisøk-table1", "rowData"),
            Output("tab-frisøk-table1", "columnDefs"),
            Input("tab-frisøk-button1", "n_clicks"),
            State("tab-frisøk-textarea1", "value"),
            State("tab-frisøk-input1", "value"),
        )
        def table_frisøk(n_clicks: int, query: str, partisjoner: str) -> tuple:
            """Execute an SQL query and update the table with results.

            Parameters
            ----------
            n_clicks : int
                Number of clicks on the "kjør" button.
            query : str
                SQL query entered by the user in the text area.
            partisjoner : str
                Partition filters entered as a dictionary string (e.g., "{'aar': [2023]}").
                Can be None if no filters are provided.

            Returns:
            --------
            A tuple containing:
            - rowData (list of dict): Records to display in the table.
            - columnDefs (list of dict): Column definitions for the table.

            Notes:
            ------
            - Column definitions hide the "row_id" column by default, if present.
            """
            if n_clicks:
                if partisjoner is not None:
                    partisjoner = ast.literal_eval(partisjoner)
                df = self.database.query(query, partition_select=partisjoner)
                columns = [
                    {
                        "headerName": col,
                        "field": col,
                        "hide": True if col == "row_id" else False,
                    }
                    for col in df.columns
                ]
                return df.to_dict("records"), columns
