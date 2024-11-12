import ssb_sirius_dash


def test_main_layout():
    result = ssb_sirius_dash.main_layout(modal_list=[], tab_list=[], variable_list=[])
    assert result is not None
