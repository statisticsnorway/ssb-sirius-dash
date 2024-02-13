import pandas as pd
from plotly.graph_objs import Figure

from ssb_sirius_dash.hb_method_aio import HbMethodAIO


# test that class Ids has a method sunburst that returns a dictionary
def test_hb_method_aio_ids() -> None:
    # create an instance of the HbMethodAIO class
    hb_method_aio = _create_sut()

    assert isinstance(hb_method_aio.ids.data_store("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.scatterplot("aio_id"), dict)

    assert isinstance(hb_method_aio.ids.p_c("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.p_u("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.p_a("aio_id"), dict)

    assert isinstance(hb_method_aio.ids.hb_filter_op("aio_id"), dict)
    assert isinstance(hb_method_aio.ids.hb_filter_value("aio_id"), dict)


def test_run_hb_method_aio() -> None:
    df = pd.DataFrame().from_records(
        [
            {
                "id": "12345",
                "x1": 42.0,
                "x2": 43.0,
            },
        ]
    )

    figure = HbMethodAIO.run_hb_method(
        data=df,
        field_id="3000",
        p_c=1,
        p_u=0.5,
        p_a=0.05,
        filter_op=">",
        filter_value=1_000_000,
    )

    assert isinstance(figure, Figure)


def test_empty_scatter_plot() -> None:
    figure = HbMethodAIO.empty_scatter_plot()

    assert isinstance(figure, Figure)


def _create_sut() -> HbMethodAIO:
    df = pd.DataFrame().from_records(
        [
            {
                "norsk_identifikator": "12345",
                "beloep": 42.0,
                "beloep_1": 43.0,
            },
        ]
    )

    return HbMethodAIO(
        data=df,
        field_id="3000",
        id_field_name="norsk_identifikator",
        x_1_name="beloep",
        x_2_name="beloep_1",
    )
