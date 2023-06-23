import xarray as xr
from datetime import datetime
import numpy as np


def convert_np_to_xr(np_array, xr_array):
    if type(np_array) != xr.DataArray:
        assert np_array.shape == xr_array.shape
        xr_new = xr.DataArray(
            data=np_array,
            dims=xr_array.dims,
            coords=xr_array.coords,
            name=xr_array.name,
            attrs=xr_array.attrs,
        )
    else:
        xr_new = np_array
    return xr_new


def apply_point_condition(data, func, args):
    args = (data,) + args
    output = xr.apply_ufunc(
        func, *args, input_core_dims=[["time"]], output_core_dims=[["time"]]
    )

    return output


def apply_spatial_condition(data, func, args):
    output = xr.map_blocks(func, data, args=args, template=data)
    return output


def reduce_datetime_precision(t, fmt="%Y-%m-%dT%H:%M:%S"):
    t = np.datetime_as_string(t).split(".000000000")[0]
    return datetime.strptime(t, fmt)
