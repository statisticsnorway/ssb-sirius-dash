import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import callback
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .modal_functions import sidebar_button


class VisualiseringsbyggerModule:
    """A module for creating and visualizing data queries and graphs interactively.

    Attributes:
    -----------
    database : object
        Database connection or interface for executing queries.
    """

    def __init__(self, database: object) -> None:
        """Initialize the VisualiseringsbyggerModule.

        Parameters
        ----------
        database : object
            The database connection or interface used for querying data.
        """
        self.database = database
        self.callbacks()

    def layout(self) -> html.Div:
        """Generate the layout for the Visualiseringsbygger module.

        Returns:
        --------
        A Div element containing components for querying data and visualizing graphs.
        """
        layout = html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("🏗️ Visualiseringsbygger"),
                        ),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    style={
                                        "display": "grid",
                                        "height": "100%",
                                        "grid-template-rows": "5% 25% 35% 5% 50%",
                                    },
                                    children=[
                                        html.Div(
                                            dbc.Button(
                                                "Kjør spørring",
                                                id="sql-button",
                                                style={
                                                    "display": "flex",
                                                    "flex-direction": "column",
                                                    "align-items": "center",
                                                    "word-break": "break-all",
                                                    "margin-bottom": "5%",
                                                    "width": "100%",
                                                },
                                            )
                                        ),
                                        html.Div(
                                            dcc.Textarea(
                                                id="sqlmodal-textarea",
                                                placeholder="SELECT * FROM databasetabell",
                                                style={"width": "100%", "height": 300},
                                            ),
                                        ),
                                        html.Div(
                                            dag.AgGrid(
                                                id="sql-output-table",
                                                className="ag-theme-alpine-dark header-style-on-filter",
                                                columnSize="responsiveSizeToFit",
                                                style={"pagination": True},
                                            )
                                        ),
                                        html.Div(
                                            style={
                                                "display": "grid",
                                                "height": "100%",
                                                "grid-template-columns": "25% 25% 25% 25%",
                                            },
                                            children=[
                                                dcc.Dropdown(
                                                    id="sql-x",
                                                    placeholder="x-aksen",
                                                    value=[],
                                                    multi=True,
                                                    className="dbc",
                                                ),
                                                dcc.Dropdown(
                                                    id="sql-y",
                                                    placeholder="y-aksen",
                                                    value=[],
                                                    multi=True,
                                                    className="dbc",
                                                ),
                                                dcc.Dropdown(
                                                    id="sql-hover",
                                                    placeholder="hoverdata",
                                                    value=[],
                                                    multi=True,
                                                    className="dbc",
                                                ),
                                                dcc.Dropdown(
                                                    id="sql-graph-type",
                                                    placeholder="graftype",
                                                    options=[
                                                        {
                                                            "label": "scatter",
                                                            "value": "scatter",
                                                        },
                                                        {
                                                            "label": "box",
                                                            "value": "box",
                                                        },
                                                        {
                                                            "label": "violin",
                                                            "value": "violin",
                                                        },
                                                        {
                                                            "label": "line",
                                                            "value": "line",
                                                        },
                                                        {
                                                            "label": "bar",
                                                            "value": "bar",
                                                        },
                                                        {
                                                            "label": "histogram",
                                                            "value": "histogram",
                                                        },
                                                    ],
                                                    className="dbc",
                                                ),
                                            ],
                                        ),
                                        dcc.Loading(
                                            id="sql-graph1-loading",
                                            children=[
                                                dcc.Graph(
                                                    id="sql-graph1", className="m-4"
                                                )
                                            ],
                                            type="graph",
                                            style={
                                                "position": "fixed",
                                                "z-index": 9999,
                                            },
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                    id="sql-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button("🏗️", "Visualiseringsbygger", "sidebar-sql-button"),
            ],
        )
        return layout

    def callbacks(self) -> None:
        """Register Dash callbacks for the Visualiseringsbygger module.

        Notes:
        ------
        - `sqlmodal_toggle` toggles the visibility of the query modal.
        - `sql_query` executes the SQL query and updates the table and dropdown options.
        - `update_graph` generates graphs based on selected columns and graph type.
        """

        @callback(
            Output("sql-modal", "is_open"),
            Input("sidebar-sql-button", "n_clicks"),
            State("sql-modal", "is_open"),
        )
        def sqlmodal_toggle(n: int, is_open: bool) -> bool:
            """Toggle the visibility of the SQL query modal.

            Parameters
            ----------
            n : int
                The number of clicks on the sidebar button.
            is_open : bool
                The current visibility state of the modal.

            Returns:
            --------
            The new visibility state of the modal.
            """
            if n:
                return not is_open
            return is_open

        @callback(
            Output("sql-output-table", "rowData"),
            Output("sql-output-table", "columnDefs"),
            Output("sql-x", "options"),
            Output("sql-y", "options"),
            Output("sql-hover", "options"),
            Input("sql-button", "n_clicks"),
            State("sqlmodal-textarea", "value"),
        )
        def sql_query(n_clicks: int, value: str) -> tuple:
            """Execute an SQL query and update table data and dropdown options.

            Parameters
            ----------
            n_clicks : int
                The number of clicks on the query execution button.
            value : str
                The SQL query string entered in the text area.

            Returns:
            --------
            A tuple containing:
            - rowData (list of dict): The table data.
            - columnDefs (list of dict): The column definitions for the table.
            - x, y, hover options (list of dict): Dropdown options for graph axes and hover data.
            """
            if n_clicks:
                df = self.database.query(f"""{value}""")
                options = [{"label": col, "value": col} for col in df.columns]
                columns = [{"headerName": col, "field": col} for col in df.columns]
                return df.to_dict("records"), columns, options, options, options

        @callback(
            Output("sql-graph1", "figure"),
            Input("sql-x", "value"),
            Input("sql-y", "value"),
            Input("sql-hover", "value"),
            Input("sql-graph-type", "value"),
            State("sql-output-table", "rowData"),
            State("sql-output-table", "columnDefs"),
        )
        def update_graph(
            x_axis: str | list,
            y_axis: str | list,
            hover_data: str | list,
            graph_type: str,
            rowData: list,
            columnDefs: list,
        ) -> dict:
            """Generate a graph based on the selected columns and graph type.

            Parameters
            ----------
            x_axis : str or list
                The column(s) selected for the x-axis.
            y_axis : str or list
                The column(s) selected for the y-axis.
            hover_data : str or list, optional
                The column(s) to display as hover data.
            graph_type : str
                The type of graph to generate (e.g., "scatter", "bar").
            rowData : list of dict
                The data displayed in the table.
            columnDefs : list of dict
                The column definitions for the table.

            Returns:
            --------
            A Plotly figure dictionary.
            """
            if x_axis and y_axis:
                if isinstance(x_axis, list) and len(x_axis) == 1:
                    x_axis = x_axis[0]
                if isinstance(y_axis, list) and len(y_axis) == 1:
                    y_axis = y_axis[0]
                if (
                    isinstance(x_axis, list)
                    and len(x_axis) > 1
                    and isinstance(y_axis, list)
                    and len(y_axis) > 1
                ):
                    y_axis = y_axis[0]
                df = pd.DataFrame(rowData)
                columns = [col["field"] for col in columnDefs]
                df.columns = columns
                df.fillna(0)
                if graph_type == "scatter":
                    fig = px.scatter(
                        df,
                        x=x_axis,
                        y=y_axis,
                        hover_data=[hover_data] if hover_data else None,
                    )
                elif graph_type == "line":
                    fig = px.line(
                        df,
                        x=x_axis,
                        y=y_axis,
                        hover_data=[hover_data] if hover_data else None,
                    )
                elif graph_type == "bar":
                    fig = px.bar(
                        df,
                        x=x_axis,
                        y=y_axis,
                        hover_data=[hover_data] if hover_data else None,
                    )
                elif graph_type == "box":
                    fig = px.box(df, x=x_axis, y=y_axis, points="all")
                elif graph_type == "violin":
                    fig = px.violin(df, x=x_axis, y=y_axis, box=True, points="all")
                elif graph_type == "histogram":
                    fig = px.histogram(
                        df,
                        x=x_axis,
                        y=y_axis,
                        hover_data=[hover_data] if hover_data else None,
                    )
                else:
                    fig = {}
                return fig
            else:
                return {}
