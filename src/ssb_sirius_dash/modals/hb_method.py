from collections.abc import Callable

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate

from ..kostra_r_wrapper import hb_method
from .modal_functions import sidebar_button

states_options = [
    {
        "aar": ("var-aar", "value"),
        "termin": ("var-termin", "value"),
        "maaned": {"var-maaned", "value"},
        "nace": ("var-nace", "value"),
        "nspekfelt": ("var-nspekfelt", "value"),
    }
]

ident_options = [
    {
        "orgb": ("var-bedrift", "value"),
        "orgf": ("var-foretak", "value"),
    }
]


class HBMethodModule:
    """Module for detecting outliers using the Hidiroglou-Berthelot (HB) method in a Dash application.

    This module applies the HB method to identify potential outliers in time-series data by comparing
    values in the current period (t) with revised values from the previous period (t-1). It includes
    methods for preprocessing data, visualizing results, and managing interactions in a Dash app.

    Attributes:
        database (object): Database connection or interface for fetching data.
        hb_get_data (callable): Function for retrieving data based on selected parameters.

    References:
        More information about the HB method:
        https://rdrr.io/github/statisticsnorway/Kostra/man/Hb.html
    """

    def __init__(
        self,
        database: object,
        hb_get_data_func: Callable,
        selected_state_keys: list[str],
        selected_ident: list[str],
        variable: str,
    ) -> None:
        """Initializes the HBMethodModule.

        Args:
            database (object): Database connection or interface to fetch relevant data.
            hb_get_data_func (Callable): Function to fetch data for processing using the HB method.
            selected_state_keys (list of str): Keys representing selected states for filtering data.
            selected_ident (list of str): Identifier used for grouping or unique identification in the data.
            variable (str): Name of the value variable to analyze using the HB method.
        """
        self.database = database
        self.hb_get_data = hb_get_data_func
        self.callbacks(selected_state_keys, selected_ident, variable)

    def make_hb_data(
        self,
        data_df: pd.DataFrame,
        pc: int,
        pu: float,
        pa: float,
        ident: str,
        variable: str,
    ) -> pd.DataFrame:
        """Processes data using the HB method for outlier detection.

        Args:
            data_df (pandas.DataFrame): Input data containing variables for analysis.
            pc (int): Confidence interval control parameter.
            pu (float): Parameter for adjusting the variable's level.
            pa (float): Parameter for small differences between quartiles and the median.
            ident (str): Identifier field name in the dataset.
            variable (str): Name of the value variable for analysis.

        Returns:
            pandas.DataFrame: Processed data with outlier results, sorted by "maxX".
        """
        hb_result = hb_method(
            data=data_df,
            p_c=pc,
            p_u=pu,
            p_a=pa,
            id_field_name=ident,
            x_1_field_name=variable,
            x_2_field_name=f"{variable}_1",
        )

        return hb_result.sort_values(by=["maxX"])

    def make_hb_figure(self, data: pd.DataFrame, variable: str) -> go.Figure:
        """Creates a Plotly figure for visualizing HB method results.

        Args:
            data (pandas.DataFrame): Processed data from the HB method, including outlier and limit values.
            variable (str): Name of the value variable for the method.

        Returns:
            plotly.graph_objects.Figure: Plotly figure with scatter plots for observations and limits.
        """
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
                    "colorscale": [[0, "#3498DB"], [1, "yellow"]],
                },
            )
        )
        fig.add_trace(go.Scatter(x=x, y=z, name="Øvre grense", marker_color="red"))
        fig.add_trace(go.Scatter(x=x, y=k, name="Nedre grense", marker_color="red"))
        fig.update_layout(
            height=800,
            title_text="HB-metoden",
            plot_bgcolor="#1F2833",
            paper_bgcolor="#1F2833",
            font_color="white",
        )
        fig.update_xaxes(title=variable, range=[0, max(x) * 1.05])
        fig.update_yaxes(title="Forholdstallet")

        return fig

    def layout(self) -> html.Div:
        """Generates the layout for the HB method Dash component.

        Returns:
            dash.html.Div: Div containing the modal and interactive elements for the HB method.
        """
        infobox = html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("HB-metoden")),
                        dbc.ModalBody(
                            "Output: All units are returned, but the HB method is only performed on the data set where units with both x1 and x2 not missing and greater than zero are included. In this data set, units with x1 = x2 are included in he HB method only if they cover less than 50 per cent of the number of units in the stratum."
                        ),
                        dbc.ModalFooter(
                            html.Button(
                                "Lukk", id="close", className="ms-auto", n_clicks=0
                            )
                        ),
                    ],
                    id="modal",
                    is_open=False,
                ),
            ]
        )

        return html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("HB-metoden")),
                        dbc.ModalBody(
                            [
                                dbc.Row(infobox),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                "Kjør HB-modell",
                                                id="hb_button",
                                                style={"height": "100%"},
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Åpne infoboks", id="open", n_clicks=0
                                            ),
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        self._build_input_field(
                                            "Skriv inn pC",
                                            "hb_pc",
                                            20,
                                            0,
                                            None,
                                            20,
                                            "Parameter that controls the length of the confidence interval.",
                                        ),
                                        self._build_input_field(
                                            "Skriv inn pu",
                                            "hb_pu",
                                            0.5,
                                            0,
                                            1,
                                            0.5,
                                            "Parameter that adjusts for different level of the variables.",
                                        ),
                                        self._build_input_field(
                                            "Skriv inn pA",
                                            "hb_pa",
                                            0.05,
                                            0,
                                            1,
                                            0.05,
                                            "Parameter that adjusts for small differences between the median and the 1st or 3rd quartile.",
                                        ),
                                    ],
                                    style={"margin": "20px"},
                                ),
                                dbc.Row(
                                    dcc.Loading(dcc.Graph(id="hb_figure")),
                                    style={"margin": "20px"},
                                ),
                            ]
                        ),
                    ],
                    id="hb-modal",
                    size="xl",
                    fullscreen="xxl-down",
                ),
                sidebar_button("🥼", "HB-Metoden", "sidebar-hb-button"),
            ]
        )

    def _build_input_field(
        self,
        label: str,
        id_name: str,
        default_value: int | float,
        min_value: int | float,
        max_value: int | float,
        initial_value: int | float,
        tooltip_text: str,
    ) -> dbc.Col:
        """Builds an input field with a tooltip for user parameter inputs.

        Args:
            label (str): Text label for the input field.
            id_name (str): Unique ID for the input field.
            default_value (int | float): Default value for the input.
            min_value (int | float): Minimum allowable value.
            max_value (int | float): Maximum allowable value.
            initial_value (int | float): Initial value to display.
            tooltip_text (str): Text description displayed in the tooltip.

        Returns:
            dash_bootstrap_components.Col: Dash Bootstrap column containing the input field and tooltip.
        """
        return dbc.Col(
            dbc.Stack(
                [
                    html.Span(
                        label,
                        id=f"{id_name}_tooltip",
                        style={
                            "textDecoration": "underline",
                            "cursor": "pointer",
                            "color": "white",
                        },
                    ),
                    dbc.Tooltip(
                        [
                            html.P(tooltip_text),
                        ],
                        target=f"{id_name}_tooltip",
                    ),
                    dcc.Input(
                        id=id_name,
                        type="number",
                        value=default_value,
                        min=min_value,
                        max=max_value,
                    ),
                ]
            )
        )

    def callbacks(
        self, selected_state_keys: list[str], selected_ident: list[str], variable: str
    ) -> None:
        """Registers callbacks for the HB method Dash app components.

        Args:
            selected_state_keys (list of str): List of state keys for dynamic state configuration.
            selected_ident (list of str): Identifier used for grouping or filtering data.
            variable (str): Name of the value variable for HB method analysis.

        Notes:
            This method registers Dash callbacks for handling user interactions, including
            running the HB method, toggling the modal, and passing results to `variabelvelger`.
        """
        states_dict = states_options[0]
        dynamic_states = [
            State(states_dict[key][0], states_dict[key][1])
            for key in selected_state_keys
        ]

        ident = ident_options[0][selected_ident]
        component_id, property_name = ident
        output_object = Output(component_id, property_name, allow_duplicate=True)

        @callback(
            Output("hb_figure", "figure"),
            Input("hb_button", "n_clicks"),
            State("hb_pc", "value"),
            State("hb_pu", "value"),
            State("hb_pa", "value"),
            *dynamic_states,
        )
        def use_hb(
            n_click: int, pc: int, pu: float, pa: float, *dynamic_states: list
        ) -> go.Figure:
            """Executes the HB method and updates the visualization.

            Args:
                n_click (int): Number of clicks on the "Run HB Model" button.
                pc (int): Confidence interval parameter.
                pu (float): Parameter for variable level adjustment.
                pa (float): Parameter for small differences between quartiles and the median.
                *dynamic_states (list): Additional state parameters for data filtering.

            Returns:
                plotly.graph_objects.Figure: Updated figure visualizing HB method results.

            Raises:
                PreventUpdate: If no button click is detected.
            """
            states_values = dynamic_states[: len(selected_state_keys)]
            state_params = {
                key: value
                for key, value in zip(selected_state_keys, states_values, strict=False)
            }

            args = []
            for key in selected_state_keys:
                var = state_params.get(key)
                if var is not None:
                    args.append(var)

            if "nace" in state_params and state_params["nace"] is not None:
                n = len(state_params["nace"])
                args.append(n)

            if n_click:
                data = self.hb_get_data(self.database, *args)
                data = self.make_hb_data(data, pc, pu, pa, selected_ident, variable)
                return self.make_hb_figure(data, variable)
            else:
                raise PreventUpdate

        @callback(
            Output("hb-modal", "is_open"),
            Input("sidebar-hb-button", "n_clicks"),
            State("hb-modal", "is_open"),
        )
        def hbmodal_toggle(n: int, is_open: bool) -> bool:
            """Toggles the state of the modal window.

            Args:
                n (int): Number of clicks on the toggle button.
                is_open (bool): Current state of the modal (open/closed).

            Returns:
                bool: New state of the modal (open/closed).
            """
            if n:
                return not is_open
            return is_open

        @callback(
            output_object,
            Input("hb_figure", "clickData"),
            prevent_initial_call=True,
        )
        def hb_to_main_table(clickdata: dict) -> str:
            """Passes the selected observation identifier to `variabelvelger`.

            Args:
                clickdata (dict): Data from the clicked point in the HB visualization.

            Returns:
                str: Identifier of the selected observation.
            """
            if clickdata:
                ident = clickdata["points"][0]["hovertext"]
                return ident
