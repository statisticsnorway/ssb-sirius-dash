import dash_bootstrap_components as dbc
from dash import dash_table, html, dcc, callback
import dash_ag_grid as dag
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from .modal_functions import sidebar_button


class VisualiseringsbyggerModule:
    def __init__(self, database):
        self.database = database
        self.callbacks()

    def layout(self):
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

    def callbacks(self):
        @callback(
            Output("sql-modal", "is_open"),
            Input("sidebar-sql-button", "n_clicks"),
            State("sql-modal", "is_open"),
        )
        def sqlmodal_toggle(n, is_open):
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
        def sql_query(n_clicks, value):
            if n_clicks > 0:
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
        def update_graph(x_axis, y_axis, hover_data, graph_type, rowData, columnDefs):
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
