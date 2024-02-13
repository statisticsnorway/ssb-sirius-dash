import uuid
from typing import Any
from typing import Optional

import pandas as pd
import plotly.express as px
from dash.dcc import Graph


class SunburstAIO(Graph):  # type: ignore
    """SunburstAIO is an All-in-One component that is composed."""

    class Ids:
        """A set of functions that create pattern-matching callbacks of the subcomponents."""

        @staticmethod
        def sunburst(aio_id: Any) -> dict[str, Any]:
            """Returns the component ID for the sunburst component.

            :param aio_id: The All-in-One component ID
            :return: The component ID for the sunburst component
            """
            return {
                "component": "SunburstAIO",
                "subcomponent": "sunburst",
                "aio_id": aio_id,
            }

    ids = Ids

    def __init__(
        self,
        data: pd.DataFrame,
        path: list[str],
        values: str,
        aio_id: Optional[str] = None,
    ) -> None:
        """SunburstAIO is an All-in-One component that is composed.

        :param data: DataFrame
        :param path: Path to show in the sunburst
        :param values: Name of value column
        :param aio_id: The All-in-One component ID used to generate the sunburst component's dictionary IDs.
        """
        self.aio_id = aio_id if aio_id else str(uuid.uuid4())

        figure = px.sunburst(data, path=path, values=values)

        figure.update_layout(
            plot_bgcolor="#1F2833",
            paper_bgcolor="#1F2833",
            font_color="#66FCF1",
            xaxis=dict(color="#66FCF1"),
            yaxis=dict(color="#66FCF1"),
        )

        super().__init__(id=self.ids.sunburst(self.aio_id), figure=figure)
