import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback, MATCH
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from kostra_r_wrapper import hb_method


class hb(html.Div):
    """
    A Dash component that encapsulates the functionality for running and interacting with the HB-method,
    a statistical technique used for detecting outliers.

    This All-In-One (AIO) component provides a user interface for configuring and running the HB-method,
    including input fields for setting parameters, buttons for executing the method, and the optional ability to 
    save and load configurations. The component also displays the results graphically, allowing users 
    to visualize detected outliers.

    Attributes:
    -----------
    ids : class
        A nested class containing methods for generating unique IDs for each subcomponent of the Hb component.

    Methods:
    --------
    hb_modal_toggle(n, is_open):
        Toggles the visibility of the modal containing the HB-method interface.

    set_hb_parameters(field):
        Sets the default or stored parameters for the HB-method based on the selected variable field.

    save_hb_settings(field, pC, pU, pA, n_click):
        Saves the current HB-method parameters to a JSON file for future use.

    _make_hb_figure(data, field):
        Creates and returns a Plotly figure that visualizes the HB-method results.

    use_hb(field, pC, pU, pA, n_click):
        Executes the HB-method using the specified parameters and updates the figure with the results.

    Notes:
    ------
    - The component supports saving and loading parameter settings if the `save_param_functionality` 
      option is enabled.
    - The `use_hb` method triggers the HB-method execution and updates the graph upon clicking the 
      corresponding button.
    """
    class ids:
        modal_button = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "modal_button",
            "aio_id": aio_id,
        }
        modal = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "modal",
            "aio_id": aio_id,
        }
        button = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "button",
            "aio_id": aio_id,
        }
        save_button = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "save_button",
            "aio_id": aio_id,
        }
        variable_store = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "variable_store",
            "aio_id": aio_id,
        }
        ident_store = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "ident_store",
            "aio_id": aio_id,
        }
        input_pu = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "input_pu",
            "aio_id": aio_id,
        }
        input_pc = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "input_pc",
            "aio_id": aio_id,
        }
        input_pa = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "input_pa",
            "aio_id": aio_id,
        }
        save_button = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "save_button",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "hb_AIO",
            "subcomponent": "graph",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(self, aio_id="hb", hotkey=None, save_param_functionality=False):
        if save_param_functionality:
            import dapla as dp
        save_button_visibility = "hidden" if not save_param_functionality else "visible"

        super().__init__(
            [
                dbc.Button("HB metoden", id=self.ids.modal_button(aio_id)),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("HB-metoden")),
                        dbc.ModalBody(
                            [
                                dcc.Store(id = self.ids.variable_store(aio_id)),
                                dcc.Store(id = self.ids.ident_store(aio_id)),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                "Kjør HB-modell",
                                                id=self.ids.button(aio_id),
                                                style={"height": "100%"},
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Lagre parametere",
                                                id=self.ids.save_button(aio_id),
                                                style={
                                                    "visibility": save_button_visibility
                                                },
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Åpne infoboks",
                                                id="open",
                                                n_clicks=0,
                                            ),
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Stack(
                                                [
                                                    html.Span(
                                                        "Skriv inn pC",
                                                        id="hb_pC_tooltip",
                                                        style={
                                                            "textDecoration": "underline",
                                                            "cursor": "pointer",
                                                            "color": "white",
                                                        },
                                                    ),
                                                    dbc.Tooltip(
                                                        [
                                                            html.P(
                                                                "Parameter that controls the length of the confidence interval."
                                                            ),
                                                            html.P("Min value: 0"),
                                                            html.P("Max value: inf"),
                                                            html.P("Default value 20."),
                                                        ],
                                                        target="hb_pC_tooltip",
                                                    ),
                                                    dcc.Input(
                                                        id=self.ids.input_pc(aio_id),
                                                        type="number",
                                                        value=20,
                                                        min=0,
                                                    ),
                                                ]
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Stack(
                                                [
                                                    html.Span(
                                                        "Skriv inn pU",
                                                        id="hb_pU_tooltip",
                                                        style={
                                                            "textDecoration": "underline",
                                                            "cursor": "pointer",
                                                            "color": "white",
                                                        },
                                                    ),
                                                    dbc.Tooltip(
                                                        [
                                                            html.P(
                                                                "Parameter that adjusts for different level of the variables."
                                                            ),
                                                            html.P("Min value: 0"),
                                                            html.P("Max value: 1"),
                                                            html.P("Default value 0.5"),
                                                        ],
                                                        target="hb_pU_tooltip",
                                                    ),
                                                    dcc.Input(
                                                        id=self.ids.input_pu(aio_id),
                                                        type="number",
                                                        value=0.5,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Stack(
                                                [
                                                    html.Span(
                                                        "Skriv inn pA",
                                                        id="hb_pA_tooltip",
                                                        style={
                                                            "textDecoration": "underline",
                                                            "cursor": "pointer",
                                                            "color": "white",
                                                        },
                                                    ),
                                                    dbc.Tooltip(
                                                        [
                                                            html.P(
                                                                "Parameter that adjusts for small differences between the median and the 1st or 3rd quartile."
                                                            ),
                                                            html.P("Min value: 0"),
                                                            html.P("Max value: 1"),
                                                            html.P(
                                                                "Default value 0.05."
                                                            ),
                                                        ],
                                                        target="hb_pA_tooltip",
                                                    ),
                                                    dcc.Input(
                                                        id=self.ids.input_pa(aio_id),
                                                        type="number",
                                                        value=0.05,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            )
                                        ),
                                    ],
                                    style={"margin": "20px"},
                                ),
                                dbc.Row(
                                    dcc.Loading(dcc.Graph(id=self.ids.graph(aio_id))),
                                    style={"margin": "20px"},
                                ),
                            ]
                        ),
                    ],
                    id=self.ids.modal(aio_id),
                    size="xl",
                    fullscreen="xxl-down",
                ),
            ]
        )

    @callback(
        Output(ids.modal(MATCH), "is_open"),
        Input(ids.modal_button(MATCH), "n_clicks"),
        State(ids.modal(MATCH), "is_open"),
    )
    def hb_modal_toggle(n, is_open):
        if n:
            return not is_open
        return is_open

    @callback(
        Output(ids.input_pc(MATCH), "value"),
        Output(ids.input_pu(MATCH), "value"),
        Output(ids.input_pa(MATCH), "value"),
        Input(ids.variable_store(MATCH), "data"),
    )
    def set_hb_parameters(field):
        default_settings = {
            "pC": 20,
            "pU": 0.5,
            "pA": 0.05,
        }
        if field is not None:
            try:
                dp.FileClient.ls(
                    f"{sfp.get_bucket('p')}{sfp.get_folder('t')}edit_settings/hb_settings.json"
                )
                with dp.FileClient.gcs_open(
                    f"{sfp.get_bucket('p')}{sfp.get_folder('t')}edit_settings/hb_settings.json",
                    "r",
                ) as outfile:
                    settings = json.load(outfile)
            except FileNotFoundError:
                settings = {}
                settings[field] = default_settings
            if field not in settings.keys():
                settings[field] = default_settings

            return settings[field]["pC"], settings[field]["pU"], settings[field]["pA"]
        else:
            return (
                default_settings["pC"],
                default_settings["pU"],
                default_settings["pA"],
            )

    @callback(
        Output(ids.save_button(MATCH), "n_clicks"),
        State(ids.variable_store(MATCH), "data"),
        State(ids.input_pc(MATCH), "value"),
        State(ids.input_pu(MATCH), "value"),
        State(ids.input_pa(MATCH), "value"),
        Input(ids.save_button(MATCH), "n_clicks"),
        prevent_initial_call=True,
    )
    def save_hb_settings(field, pC, pU, pA, n_click):
        if n_click:
            try:
                dp.FileClient.ls(
                    f"{sfp.get_bucket('p')}{sfp.get_folder('t')}edit_settings/hb_settings.json"
                )
                with dp.FileClient.gcs_open(
                    f"{sfp.get_bucket('p')}{sfp.get_folder('t')}edit_settings/hb_settings.json",
                    "r",
                ) as outfile:
                    settings = json.load(outfile)
            except FileNotFoundError:
                settings = {}
            settings[field] = {
                "pC": pC,
                "pU": pU,
                "pA": pA,
            }
            with dp.FileClient.gcs_open(
                f"{sfp.get_bucket('p')}{sfp.get_folder('t')}edit_settings/hb_settings.json",
                "w",
            ) as outfile:
                json.dump(settings, outfile)
            return None
        else:
            raise PreventUpdate

    def _make_hb_figure(data, field):
        x = data["maxX"]
        y = data["ratio"]
        z = data["upperLimit"]
        k = data["lowerLimit"]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                hovertext=data["id"],
                name="Observasjon",
                marker={
                    "color": data["outlier"],
                    "colorscale": [[0, "#526074"], [1, "#b71e1d"]],
                },
            )
        )
        fig.add_trace(go.Scatter(x=x, y=z, name="Øvre grense", marker_color="red"))
        fig.add_trace(go.Scatter(x=x, y=k, name="Nedre grense", marker_color="red"))
        fig.update_layout(
            height=800,
            title_text="HB metoden",
        )
        fig.update_xaxes(title=field, range=[0, max(x) * 1.05])
        fig.update_yaxes(title="Forholdstallet")

        return fig

    @callback(
        Output(ids.graph(MATCH), "figure"),
        State(ids.variable_store(MATCH), "data"),
        State(ids.input_pc(MATCH), "value"),
        State(ids.input_pu(MATCH), "value"),
        State(ids.input_pa(MATCH), "value"),
        Input(ids.button(MATCH), "n_clicks"),
    )
    def use_hb(field, pC, pU, pA, n_click):
        if n_click:
            data = sfp.duckdb_til_df(filtrere="Ja")
            data = data.loc[data["felt"] == field]
            data = hb_method(data, pC, pU, pA)
            return _make_hb_figure(data, field)
        else:
            raise PreventUpdate

    @callback(
        Output(ids.ident_store(MATCH), "data"),
        Input(ids.graph(MATCH), "clickData"),
        prevent_initial_call=True,
    )
    def hb_to_main_table(clickdata):
        if clickdata:
            ident = clickdata["points"][0]["hovertext"]
            return ident