import uuid

import pandas as pd
import plotly.express as px
from dash import dcc


class SunburstAIO(dcc.Graph):
    class Ids:
        @staticmethod
        def sunburst(aio_id):
            return {
                'component': 'SunburstAIO',
                'subcomponent': 'sunburst',
                'aio_id': aio_id
            }

    ids = Ids

    def __init__(
            self,
            data: pd.DataFrame,
            path: list[str],
            values: str,
            aio_id: str = None,
    ):
        self.aio_id = aio_id if aio_id else str(uuid.uuid4())

        figure = px.sunburst(data,
                             path=path,
                             values=values)

        figure.update_layout(
            plot_bgcolor="#1F2833",
            paper_bgcolor="#1F2833",
            font_color="#66FCF1",
            xaxis=dict(color="#66FCF1"),
            yaxis=dict(color="#66FCF1"),
        )

        super().__init__(
            id=self.ids.sunburst(self.aio_id),
            figure=figure
        )
