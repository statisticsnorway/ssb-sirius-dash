from unittest import mock
from unittest.mock import Mock

import pandas as pd
from plotly.graph_objs import Figure

from ssb_sirius_dash.hb_method_aio import HbMethodAIO


# test that class Ids has a method sunburst that returns a dictionary
@mock.patch("ssb_sirius_dash.hb_method_aio.th_error")
def test_hb_method_aio_ids(th_error_mock: Mock) -> None:
    th_error_mock.return_value = pd.DataFrame().from_records(
        [
            {
                "id": "12345",
                "x1": 42.0,
                "x2": 43.0,
                "outlier": 0,
            },
        ]
    )

    # create an instance of the HbMethodAIO class
    hb_method_aio = HbMethodAIO(
        data=DF_IN_TEST,
        field_id="3000",
        id_field_name="norsk_identifikator",
        x_1_name="beloep",
        x_2_name="beloep_1",
    )

    assert isinstance(hb_method_aio.ids.data_store("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.scatterplot("aio_id"), dict)

    assert isinstance(hb_method_aio.ids.p_c("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.p_u("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.p_a("aio_id"), dict)

    assert isinstance(hb_method_aio.ids.hb_filter_op("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.hb_filter_value("aio_id"), dict)

    # assert mock call
    th_error_mock.assert_called_once_with(
        data=DF_IN_TEST,
        id_field_name="norsk_identifikator",
        x_1_field_name="beloep",
        x_2_field_name="beloep_1",
    )


@mock.patch("ssb_sirius_dash.hb_method_aio.hb_method")
def test_run_hb_method_aio(hb_method_mock: Mock) -> None:
    hb_method_mock.return_value = pd.DataFrame().from_records(
        [
            {
                "id": "12345",
                "outlier": 1,
                "maxX": 40.0,
                "lowerLimit": 4.0,
                "upperLimit": 40.0,
                "ratio": 10.0,
            },
        ]
    )

    input_df = pd.DataFrame().from_records(
        [
            {
                "id": "12345",
                "x1": 40.0,
                "x2": 4.0,
            },
        ]
    )

    figure = HbMethodAIO.run_hb_method(
        data=input_df,
        field_id="3000",
        p_c=1,
        p_u=0.5,
        p_a=0.05,
        filter_op=">",
        filter_value=1_000_000,
    )

    assert isinstance(figure, Figure)

    # assert mock call
    hb_method_mock.assert_called_once_with(
        data=input_df,
        p_c=1,
        p_u=0.5,
        p_a=0.05,
        id_field_name="id",
        x_1_field_name="x1",
        x_2_field_name="x2",
    )


def test_empty_scatter_plot() -> None:
    figure = HbMethodAIO.empty_scatter_plot()

    assert isinstance(figure, Figure)


DF_IN_TEST = pd.DataFrame().from_records(
    [
        {
            "norsk_identifikator": "12345",
            "beloep": 42.0,
            "beloep_1": 43.0,
        },
    ]
)
