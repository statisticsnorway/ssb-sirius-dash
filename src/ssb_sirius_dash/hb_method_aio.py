import uuid

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, callback, Input, Output, MATCH, State
from dash.html import Figure
from plotly.graph_objs import Scatter, scatter
from rpy2.robjects import default_converter, conversion, pandas2ri

from .r_utils import get_kostra_r


class HbMethodAIO(html.Div):
    class Ids:
        @staticmethod
        def data_store(aio_id: str) -> dict:
            """
            Returns the component ID for the data store.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'data_store',
                'aio_id': aio_id
            }

        @staticmethod
        def scatterplot(aio_id: str) -> dict:
            """
            Returns the component ID for the scatterplot.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'scatterplot',
                'aio_id': aio_id
            }

        @staticmethod
        def p_c(aio_id: str) -> dict:
            """
            Returns the component ID for the pC dropdown.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'p_c',
                'aio_id': aio_id
            }

        @staticmethod
        def p_u(aio_id: str) -> dict:
            """
            Returns the component ID for the pU dropdown.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'p_u',
                'aio_id': aio_id
            }

        @staticmethod
        def p_a(aio_id: str) -> dict:
            """
            Returns the component ID for the pA dropdown.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'p_a',
                'aio_id': aio_id
            }

        @staticmethod
        def hb_filter_op(aio_id: str) -> dict:
            """
            Returns the component ID for the filter operator dropdown.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'hb_filter_op',
                'aio_id': aio_id
            }

        @staticmethod
        def hb_filter_value(aio_id: str) -> dict:
            """
            Returns the component ID for the filter value dropdown.
            :param aio_id: Component aio-ID
            :return: Component ID
            """
            return {
                'component': 'HbMethodAIO',
                'subcomponent': 'hb_filter_value',
                'aio_id': aio_id
            }

    ids = Ids

    @staticmethod
    def run_th_error(data: pd.DataFrame,
                     id_field_name: str,
                     x_1_name: str,
                     x_2_name: str) -> pd.DataFrame:
        """
        Runs the TH-error method on the data.
        :param data: Dataframe with the data
        :param id_field_name: Field name for the ID
        :param x_1_name: X1 field name
        :param x_2_name: X2 field name
        :return: Dataframe without outliers
        """
        with conversion.localconverter(default_converter + pandas2ri.converter):
            th_error_result = get_kostra_r().ThError(
                data=data,
                id=id_field_name,
                x1=x_1_name,
                x2=x_2_name
            )
            return th_error_result[th_error_result.outlier == 0]

    @staticmethod
    def run_hb_method(data: pd.DataFrame,
                      field_id: int,
                      p_c: int,
                      p_u: float,
                      p_a: float,
                      filter_op: str,
                      filter_value: int) -> Figure:
        """"
        Runs the HB-method on the data.
        :param data: Dataframe with the data
        :param field_id: Field ID
        :param p_c: pC value
        :param p_u: pU value
        :param p_a: pA value
        :param filter_op: Filter operator
        :param filter_value: Filter value
        :return: Figure for the scatterplot
        """
        with conversion.localconverter(default_converter + pandas2ri.converter):
            hb_metoden_df = get_kostra_r().Hb(
                data=data,
                id="id",
                x1="x1",
                x2="x2",
                pC=p_c,
                pU=p_u,
                pA=p_a
            )

            df_query = f"outlier == 1 & maxX {filter_op} {filter_value}"
            significant_outliers = hb_metoden_df.query(df_query)
            significant_outliers = significant_outliers.sort_values(by=["maxX"])

            x = significant_outliers["maxX"]
            z = significant_outliers["upperLimit"]
            k = significant_outliers["lowerLimit"]

            scatter_plot = px.scatter(
                significant_outliers,
                x="maxX",
                y="ratio",
                title=f"Post {field_id} - outliers med HB-metoden ({len(significant_outliers)} stk.)",
            )

            scatter_plot.add_trace(Scatter(
                x=x,
                y=z,
                name="Øvre grense",
                mode="lines",
                line=scatter.Line(color="yellow"),
                showlegend=True)
            )

            scatter_plot.add_trace(Scatter(
                x=x,
                y=k,
                name="Nedre grense",
                mode="lines",
                line=scatter.Line(color="red"),
                showlegend=True)
            )

            hover_template = ("Norsk-ID: <b>%{customdata}</b>"
                              "<br>Beløp i hele 1000: <b>%{x}</b>"
                              "<br>Forholdstall (ratio): <b>%{y}</b>")

            scatter_plot.update_traces(
                customdata=significant_outliers['id'],
                hovertemplate=hover_template
            )

            scatter_plot.update_layout(
                xaxis_title="Beløp i hele 1000",
                yaxis_title="Forholdstall",
                plot_bgcolor="#1F2833",
                paper_bgcolor="#1F2833",
                font_color="#66FCF1",
                xaxis=dict(color="#66FCF1", hoverformat=',.2f'),
                yaxis=dict(color="#66FCF1", hoverformat=',.2f')
            )
            return scatter_plot

    @staticmethod
    def empty_scatter_plot() -> Figure:
        """
        Creates a blank figure for use when no data is available.
        :return: Figure
        """
        empty_scatter_plot = px.scatter(x=[])
        empty_scatter_plot.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        empty_scatter_plot.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        empty_scatter_plot.update_layout(
            plot_bgcolor="#1F2833",
            paper_bgcolor="#1F2833",
            xaxis=dict(color="#1F2833"),
            yaxis=dict(color="#1F2833"),
        )

        return empty_scatter_plot

    def __init__(
        self,
        data: pd.DataFrame,
        field_id: int,

        id_field_name: str,
        x_1_name: str,
        x_2_name: str,

        default_p_c: int = 100,
        default_p_u: float = 0.5,
        default_p_a: float = 0.05,

        default_filter_op: str = "<",
        default_filter_value: int = 100_000,

        aio_id: str | None = None
    ):
        """
        Creates a new HbMethodAIO component.
        :param data:
        :param field_id:
        :param id_field_name:
        :param x_1_name:
        :param x_2_name:
        :param default_p_c:
        :param default_p_u:
        :param default_p_a:
        :param default_filter_op:
        :param default_filter_value:
        :param aio_id:
        """
        self.aio_id = aio_id if aio_id else str(uuid.uuid4())

        th_result = HbMethodAIO.run_th_error(data, id_field_name, x_1_name, x_2_name)

        data_dict = {
            "df": th_result.to_dict("records"),
            "field_id": field_id
        }

        super().__init__(
            children=[
                dcc.Store(
                    data=data_dict,
                    id=self.ids.data_store(self.aio_id)
                ),
                dbc.Row(
                    id="hb-parameters",
                    className="m-2",
                    children=[
                        dbc.Col(
                            html.Span("HB-parametere (pC, pU, pA):"),
                            className="align-self-center"
                        ),
                        dbc.Col(
                            dbc.Select(
                                id=self.ids.p_c(self.aio_id),
                                options=[5, 10, 15, 20, 25, 30, 35, 40,
                                         45, 50,
                                         100, 150],
                                value=default_p_c,
                                className="m-2",
                                size="sm",
                                persistence=True
                            )
                        ),
                        dbc.Col(
                            dbc.Select(
                                id=self.ids.p_u(self.aio_id),
                                options=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
                                         0.7, 0.8,
                                         0.9],
                                value=default_p_u,
                                className="m-2",
                                size="sm",
                                persistence=True
                            )
                        ),
                        dbc.Col(
                            dbc.Select(
                                id=self.ids.p_a(self.aio_id),
                                options=[0.01, 0.02, 0.03, 0.04, 0.05,
                                         0.06, 0.07,
                                         0.08, 0.09],
                                value=default_p_a,
                                className="m-2",
                                size="sm",
                                persistence=True
                            )
                        )
                    ]
                ),
                dbc.Row(
                    id="filter-options",
                    className="m-2",
                    children=[
                        dbc.Col(
                            html.Span("Filter (etter HB):"),
                            className="align-self-center"
                        ),
                        dbc.Col(
                            dbc.Select(
                                id=self.ids.hb_filter_op(self.aio_id),
                                options=[
                                    {'label': 'Større enn',
                                     'value': '>'},
                                    {'label': 'Mindre enn',
                                     'value': '<'},
                                ],
                                value=default_filter_op,
                                className="m-2",
                                size="sm",
                                persistence=True
                            )
                        ),
                        dbc.Col(
                            dbc.Select(
                                id=self.ids.hb_filter_value(self.aio_id),
                                options=[
                                    {'label': '100 MNOK',
                                     'value': '100000'},
                                    {'label': '10 MNOK',
                                     'value': '10000'},
                                    {'label': '1 MNOK',
                                     'value': '1000'},
                                    {'label': '0,1 MNOK',
                                     'value': '100'}
                                ],
                                value=default_filter_value,
                                className="m-2",
                                size="sm",
                                persistence=True
                            )
                        )
                    ]
                ),

                dcc.Graph(
                    id=self.ids.scatterplot(self.aio_id),
                    figure=HbMethodAIO.empty_scatter_plot()
                )
            ]
        )

    # noinspection PyMethodParameters
    @callback(
        Output(ids.scatterplot(MATCH), "figure"),
        [
            Input(ids.p_c(MATCH), "value"),
            Input(ids.p_u(MATCH), "value"),
            Input(ids.p_a(MATCH), "value"),
            Input(ids.hb_filter_op(MATCH), "value"),
            Input(ids.hb_filter_value(MATCH), "value"),
            State(ids.data_store(MATCH), "data")
        ]
    )
    def update_figures_cb(p_c: str,
                          p_u: str,
                          p_a: str,
                          filter_operator: str,
                          filter_value: str,
                          data) -> Figure:
        """
        Updates the scatterplot figure.

        :param p_c: pC value
        :param p_u: pU value
        :param p_a: pA value

        :param filter_operator:
        :param filter_value:

        :param data: data from the store

        :return: figure for the scatterplot
        """

        return HbMethodAIO.run_hb_method(
            data=pd.DataFrame(data['df']),
            field_id=data['field_id'],
            p_c=int(p_c),
            p_u=float(p_u),
            p_a=float(p_a),
            filter_op=str(filter_operator),
            filter_value=int(filter_value)
        )
