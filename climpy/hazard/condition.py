from abc import ABC, abstractmethod
from typing import List
import operator

import xarray as xr
import numpy as np
import scipy as sp
import geopandas
import rioxarray
from shapely.geometry import mapping

from climpy.hazard.utils import convert_np_to_xr, apply_point_condition, apply_spatial_condition

class HazardCondition(ABC):
    @abstractmethod
    def __call__(self, data):
        pass

class PointHazardCondition(HazardCondition):
    def __call__(self, data):
        out = apply_point_condition(data, self.func, self.args)
        out = convert_np_to_xr(out, data)
        return out.transpose("time", ...)

class SpatialHazardCondition(HazardCondition):
    def __call__(self, data):
        out = apply_spatial_condition(data, self.func, self.args)
        out = convert_np_to_xr(out, data)
        return out.transpose("time", ...)


class ArealHazardCondition(SpatialHazardCondition):
    pass
    
class VolumeHazardCondition(SpatialHazardCondition):
    pass

################ Point Hazard Conditions ########################

class ThresholdQuantile(PointHazardCondition):
    def __init__(self, operator_str:str, quantile:float) -> None:
        
        operators = {
        '>': operator.gt,
        '<': operator.lt
        }

        if operator_str in operators:
            comparision_operator = operators[operator_str]
            func = lambda x : xr.where(comparision_operator(x, np.nanpercentile(x, 100*quantile)) , 1, 0)
        else:
            raise ValueError(f"operator_str should be one of '>' or '<' instead of {operator_str}")

        args = ()

        self.func = func
        self.args = args

        self.returns_event = False #! Need to automate this at some point.

################ Areal Hazard Condtions ########################

class ConnectStructure(VolumeHazardCondition):
    def __init__(self, structure:np.array) -> None:
        
        args = (structure,)

        func = lambda x, *args: sp.ndimage.label(x, *args)[0]

        self.func = func
        self.args = args

        self.returns_event = True #! Need to automate this at some point.
   
class MaskArea(ArealHazardCondition):
    def __init__(self, shp_path:str) -> None:
        shp = geopandas.read_file(shp_path)
        self.args = (shp,)
        
        def func(x, shp):
            x.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
            x.rio.write_crs("epsg:4326", inplace=True)
            clipped = x.rio.clip(shp.geometry.apply(mapping), shp.crs, drop=False)
            return clipped
   
        self.func = func

        self.returns_event = False  #! Need to automate this at some point.


class AverageArea(ArealHazardCondition):
    def __init__(self) -> None:


        func = lambda x : x.sum(dim=["lat", "lon"]) 

        self.func = func
        self.args = ( )
    
################ Volume Hazard Condtions ########################

class Sequence():
    def __init__(self, sequence):
        self.sequence = sequence