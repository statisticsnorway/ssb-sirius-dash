import logging

import pandas as pd
from rpy2.robjects import conversion
from rpy2.robjects import default_converter
from rpy2.robjects import pandas2ri

logger = logging.getLogger(__name__)


def th_error(
    data: pd.DataFrame, id_field_name: str, x_1_field_name: str, x_2_field_name: str
) -> pd.DataFrame:
    """Runs the ThError method from the R package Kostra.

    :param data: The data to run the method on
    :param id_field_name: The name of the id field
    :param x_1_field_name: The name of the first x field
    :param x_2_field_name: The name of the second x field
    :return: The result of the method
    """
    with conversion.localconverter(default_converter + pandas2ri.converter):
        th_error_result = _get_kostra_r().ThError(
            data=data, id=id_field_name, x1=x_1_field_name, x2=x_2_field_name
        )
        return th_error_result[th_error_result.outlier == 0]
