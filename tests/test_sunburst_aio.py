import pandas as pd
from src.ssb_sirius_dash.sunburst_aio import SunburstAIO


# test that class Ids has a method sunburst that returns a dictionary
def test_sunburst_aio_ids_sunburst() -> None:
    # create an instance of the SunburstAIO class
    sunburst_aio = SunburstAIO(
        data=pd.DataFrame().from_records(
            [
                {"gruppe": "A", "korttype": "B", "felt": "C", "beloep": 1},
                {"gruppe": "A", "korttype": "B", "felt": "D", "beloep": 2},
                {"gruppe": "A", "korttype": "E", "felt": "F", "beloep": 3},
            ]
        ),
        path=["gruppe", "korttype", "felt"],
        values="beloep"
    )

    # test that the sunburst method returns a dictionary
    assert isinstance(sunburst_aio.ids.sunburst("aio_id"), dict)
