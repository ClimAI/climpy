import xarray as xr
import pandas as pd
import numpy as np

def _create_areal_xarray(lon , lat, time, var):
    reference_time = pd.Timestamp("1994-01-24")   
    data = xr.DataArray(
    data=var,
    dims=["lon", "lat", "time"],
    coords=dict(
        lon=(["lon"], lon),
        lat=(["lat"], lat),
        time=(["time"], time),
        reference_time = reference_time
    ),
    attrs=dict(
        description="Test Var",
        units="[-]",
    ),
    )

    return data.transpose("time", ...)

def _create_point_xarray(time, var):

    reference_time = pd.Timestamp("1994-01-24")   
    data = xr.DataArray(
    data=var,
    dims=["time"],
    coords=dict(
        time=(["time"], time),
        reference_time = reference_time
    ),
    attrs=dict(
        description="Test Var",
        units="[-]",
    ),
    )
    return data.transpose("time", ...)

def test_areal_xarray_small(var = np.tile(np.arange(100), reps=(64,32,1))):
    
    lat = np.linspace(-16, 16, 32)
    lon = np.linspace(-32, 32, 64)
    time = pd.date_range("1994-01-24", periods=100)

    return _create_areal_xarray(lon, lat, time, var)

def test_areal_xarray_medium(var = np.tile(np.arange(1000), reps=(360,180,1))):

    lat = np.linspace(-90, 90, 180)
    lon = np.linspace(-180, 180, 360)
    time = pd.date_range("1994-01-24", periods=1000)

    return _create_areal_xarray(lon, lat, time, var)

def custom_areal_xarray(var = np.tile(np.arange(2), reps=(3,3,1))):
    
    lat = np.arange(var.shape[1])
    lon = np.arange(var.shape[0])
    time = pd.date_range("1994-01-24", periods=var.shape[2])

    return _create_areal_xarray(lon, lat, time, var)

def custom_point_xarray(var = np.arange(3)):
    time = pd.date_range("1994-01-24", periods=var.shape[0])

    return _create_point_xarray(time, var)