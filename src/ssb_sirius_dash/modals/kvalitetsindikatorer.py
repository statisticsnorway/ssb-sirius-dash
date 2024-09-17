import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate

from .modal_functions import sidebar_button


class KvalitetsindikatorerModule:
    """indicators: list
    List of indicators to include.
    """

    def __init__(self, indicators):

        self.indicators = indicators
        self.callbacks()

    def layout(self):
        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader([dbc.ModalTitle("kvalitetsindikatorer")]),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    [indicator.card for indicator in self.indicators],
                                    style={
                                        "display": "grid",
                                        "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                                        "gridGap": "20px",
                                    },
                                )
                            ]
                        ),
                    ],
                    id="kvalitetsindikatorer-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button(
                    "🎯", "Kvalitetsindikatorer", "sidebar-kvalitetsindikatorer-button"
                ),
            ]
        )

    def callbacks(self):
        @callback(
            Output("kvalitetsindikatorer-modal", "is_open"),
            Input("sidebar-kvalitetsindikatorer-button", "n_clicks"),
            State("kvalitetsindikatorer-modal", "is_open"),
        )
        def makrotabellmodal_toggle(n, is_open):
            if n:
                return not is_open
            return is_open


class KvalitetsindikatorEditeringsandel:
    """ """

    def __init__(
        self,
        get_current_data_func,
        get_change_data_func,
        periode,
        var_name,
        grouping_vars,
        ident_var,
        database,
        key_vars=None,
    ):
        self.periode = periode
        self.ident_var = ident_var
        self.var_name = var_name
        self.grouping_vars = grouping_vars
        self.get_current_data = get_current_data_func
        self.get_change_data = get_change_data_func
        self.database = database
        if key_vars:
            self.key_vars = key_vars  # TODO

        self.callbacks()

        self.card = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5("1 - Editeringsandel", className="card-title"),
                                dcc.Graph(
                                    figure=go.Figure(
                                        go.Indicator(
                                            mode="number+delta",
                                            value=self.editeringsandel(
                                                self.database, self.periode
                                            ),
                                            number={"prefix": ""},
                                            # delta={"position": "bottom", "reference": self.editeringsandel(self.periode-1)}, # TODO
                                            domain={"x": [0, 1], "y": [0, 1]},
                                        )
                                    ).update_layout(
                                        height=150,
                                        margin=dict(l=20, r=20, t=20, b=20),
                                    ),
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Detaljer",
                                id="kvalitet-editeringsandel-button-details",
                            )
                        ),
                    ],
                    style={
                        "width": "18rem",
                        "margin": "10px",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("1 - Editeringsandel"),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    children=[
                                        dcc.Dropdown(
                                            id="kvalitet-editeringsandel-dropdown",
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [var_name, *grouping_vars]
                                            ],
                                        )
                                    ],
                                ),
                                dcc.Loading(
                                    id="kvalitet-editeringsandel-details",
                                ),
                            ]
                        ),
                    ],
                    id="editeringsandel-modal",
                ),
            ]
        )

    def editeringsandel(self, database, periode):
        total = pd.DataFrame(
            self.get_current_data(database, periode).agg({self.ident_var: "nunique"})
        )
        changes = pd.DataFrame(
            self.get_change_data(database, periode).agg({self.ident_var: "nunique"})
        )
        return (changes / total * 100).iloc[0][0]

    def editeringsandel_details(self, group, database, periode):
        if isinstance(group, str):
            group = [group]
        total = (
            self.get_current_data(database, periode, group)
            .groupby(group)
            .agg({self.ident_var: "nunique"})
            .rename(columns={self.ident_var: "units"})
        )
        changes = (
            self.get_change_data(database, periode, group)
            .groupby(group)
            .agg({self.ident_var: "nunique"})
            .rename(columns={self.ident_var: "edited_units"})
        )
        c = pd.merge(total, changes, on=group, how="left").fillna(0)
        c["editeringsandel"] = c["edited_units"] / c["units"] * 100
        return c.reset_index()

    def callbacks(self):
        @callback(
            Output("editeringsandel-modal", "is_open"),
            Input("kvalitet-editeringsandel-button-details", "n_clicks"),
            State("editeringsandel-modal", "is_open"),
        )
        def kvalitetediteringsandel_modaltoggle(n, is_open):
            if n:
                return not is_open
            return is_open

        @callback(
            Output("kvalitet-editeringsandel-details", "children"),
            Input("kvalitet-editeringsandel-dropdown", "value"),
        )
        def editeringsandel_detailed(grouping_var):
            if grouping_var:
                detail_data = self.editeringsandel_details(
                    grouping_var, self.database, self.periode
                )
                return dcc.Graph(
                    figure=px.bar(
                        detail_data,
                        x="editeringsandel",
                        y=grouping_var,
                        orientation="h",
                    )
                )
            else:
                raise PreventUpdate


class KvalitetsindikatorEffektaveditering:
    """ """

    def __init__(
        self,
        get_current_data_func,
        get_original_data_func,
        periode,
        key_vars,
        grouping_vars,
        database,
    ):
        self.get_current_data = get_current_data_func
        self.get_original_data = get_original_data_func
        self.periode = periode
        self.key_vars = key_vars
        self.grouping_vars = grouping_vars
        self.database = database

        self.callbacks()

        self.card = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5(
                                    "4 - Effekten av editering", className="card-title"
                                ),
                                dcc.Graph(
                                    figure=go.Figure(
                                        go.Indicator(
                                            mode="number+delta",
                                            value=self.get_comparison_data(
                                                self.periode
                                            )["effekt av editering"][0],
                                            number={"prefix": ""},
                                            # delta={"position": "bottom", "reference": self.editeringsandel(self.periode-1)}, # TODO
                                            domain={"x": [0, 1], "y": [0, 1]},
                                        )
                                    ).update_layout(
                                        height=150,
                                        margin=dict(l=20, r=20, t=20, b=20),
                                    ),
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Detaljer",
                                id="kvalitet-effekt-button-details",
                            )
                        ),
                    ],
                    style={
                        "width": "18rem",
                        "margin": "10px",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("4 - Effekten av editering"),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    children=[
                                        dcc.Dropdown(
                                            id="kvalitet-effekt-dropdown",
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [*grouping_vars]
                                            ],
                                        )
                                    ],
                                ),
                                dcc.Loading(
                                    id="kvalitet-effekt-details",
                                ),
                            ]
                        ),
                    ],
                    id="effekt-modal",
                ),
            ]
        )

    def get_comparison_data(self, periode, grouping=None):
        if grouping is None:
            grouping = []
        elif isinstance(grouping, str):
            grouping = [grouping]
        edited = (
            self.get_current_data(self.database, periode)
            .melt(id_vars=["oppgavegivernummer", *grouping], value_vars=self.key_vars)
            .groupby([*grouping, "variable"])
            .agg({"value": "sum"})
            .rename(columns={"value": "editert"})
            .reset_index()
        )

        ueditert = (
            self.get_original_data(self.database, periode)
            .melt(id_vars=["oppgavegivernummer", *grouping], value_vars=self.key_vars)
            .groupby([*grouping, "variable"])
            .agg({"value": "sum"})
            .rename(columns={"value": "ueditert"})
            .reset_index()
        )

        merged = edited.merge(ueditert, on=[*grouping, "variable"])

        merged["effekt av editering"] = (
            (merged["ueditert"] - merged["editert"]) / merged["editert"] * 100
        )

        return merged

    def callbacks(self):
        @callback(
            Output("effekt-modal", "is_open"),
            Input("kvalitet-effekt-button-details", "n_clicks"),
            State("effekt-modal", "is_open"),
        )
        def kvaliteteffekt_modaltoggle(n, is_open):
            if n:
                return not is_open
            return is_open

        @callback(
            Output("kvalitet-effekt-details", "children"),
            Input("kvalitet-effekt-dropdown", "value"),
        )
        def kvalitet_effekt_detailed(grouping_var):
            if grouping_var:
                detail_data = self.get_comparison_data(self.periode, grouping_var)
                return dcc.Graph(
                    figure=px.bar(
                        detail_data,
                        x="effekt av editering",
                        y=grouping_var,
                        orientation="h",
                    )
                )
            else:
                raise PreventUpdate
