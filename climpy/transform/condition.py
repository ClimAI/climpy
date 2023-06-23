from abc import ABC, abstractmethod
import operator

import xarray as xr
import numpy as np
import scipy as sp
import geopandas
import rioxarray  # noqa F401
from shapely.geometry import mapping

from climpy.transform.utils import (
    convert_np_to_xr,
    apply_point_condition,
    apply_spatial_condition,
)


class Condition(ABC):
    @abstractmethod
    def __call__(self, data):
        pass


class PointCondition(Condition):
    def __call__(self, data):
        assert (
            len(data.dims) == 1 and data.dims[0] == "time"
        ), f"PointCondition can only have ('time') dimension instead  \
        of {data.dims}"
        out = apply_point_condition(data, self.func, self.args)
        out = convert_np_to_xr(out, data)
        return out.transpose("time", ...)


class SpatialCondition(Condition):
    def __call__(self, data):
        out = apply_spatial_condition(data, self.func, self.args)
        out = convert_np_to_xr(out, data)
        return out.transpose("time", ...)


class ArealCondition(SpatialCondition):
    pass


class VolumeCondition(SpatialCondition):
    pass


class PolymorphicCondition(Condition):
    pass


# =============== Point Conditions===============


class ThresholdQuantile(PointCondition):
    def __init__(self, operator_str: str, quantile: float) -> None:
        operators = {">": operator.gt, "<": operator.lt}

        if operator_str in operators:
            comparision_operator = operators[operator_str]
            func = lambda x: xr.where(  # noqa E731
                comparision_operator(x, np.nanpercentile(x, 100 * quantile)), 1, 0
            )  # noqa E731
        else:
            raise ValueError(
                f"operator_str should be one of '>' or '<' instead of {operator_str}"
            )

        args = ()

        self.func = func
        self.args = args

        self.returns_event = False  # ! Need to automate this at some point.


# ===============Areal Condtions===============


class ConnectStructure(VolumeCondition):
    def __init__(self, structure: np.array) -> None:
        args = (structure,)

        func = lambda x, *args: sp.ndimage.label(x, *args)[0]  # noqa E731

        self.func = func
        self.args = args

        self.returns_event = True  # ! Need to automate this at some point.


class MaskArea(ArealCondition):
    def __init__(self, shp_path: str) -> None:
        shp = geopandas.read_file(shp_path)
        self.args = (shp,)

        def func(x, shp):
            x.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
            x.rio.write_crs("epsg:4326", inplace=True)
            clipped = x.rio.clip(shp.geometry.apply(mapping), shp.crs, drop=False)
            return clipped

        self.func = func

        self.returns_event = False  # ! Need to automate this at some point.


class AverageArea(ArealCondition):
    def __init__(self) -> None:
        func = lambda x: x.mean(dim=["lat", "lon"])  # noqa E731

        self.func = func
        self.args = ()


# ===============Volume Condtions===============


class Sequence:
    def __init__(self, sequence):
        self.sequence = sequence
