import numpy as np
import pytest
from climpy.transform.condition import ThresholdQuantile

from tests.utils import custom_point_xarray

# Custom array of shape [2x2x2]
# inp_arr = np.array([[[-2, -1], [1, 1]],[[2, 3], [5, 4]]])
# input = custom_areal_xarray(inp_arr)
# output_arr = np.array([[[0, 0], [0, 0]],[[0, 0], [1, 0]]])
# output = custom_areal_xarray(output_arr)

# @pytest.mark.parametrize(
#     "operator_str, quantile, input, output",
#     [
#         ('>', 0.90, input, output),
#     ]
# )

inp_1 = custom_point_xarray(np.array([1, 2, 3]))
out_1 = custom_point_xarray(np.array([0, 0, 1]))

inp_2 = custom_point_xarray(np.array([1, 2, 2]))
out_2 = custom_point_xarray(np.array([0, 0, 0]))

inp_3 = custom_point_xarray(np.array([2, 2, 2]))
out_3 = custom_point_xarray(np.array([0, 0, 0]))


@pytest.mark.parametrize(
    "operator_str, quantile, input, output",
    [
        (">", 0.90, inp_1, out_1),
        (">", 0.90, inp_2, out_2),
        (">", 0.90, inp_3, out_3),
    ],
)
def test_threshold_quantile(operator_str, quantile, input, output):
    result = ThresholdQuantile(operator_str, quantile)(input)

    assert result.equals(output), f"Expected {result.values} == {output.values}"
