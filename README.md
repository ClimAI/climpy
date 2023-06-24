
<center> <img src="climpy.png" alt="logo" style="width:250px;"/></center> 

![Build Badge](https://github.com/climai/climpy/actions/workflows/python-app.yml/badge.svg)
![codecov](https://codecov.io/gh/ClimAI/climpy/branch/main/graph/badge.svg?token=VFWB1PVALY)

Climpy helps you to work with climata data to analyse climate related event. The functionalities include
- Finding temporal or spatio-temporal events defined by a `preset conditions` or defining your conditions
- Selecting events based on some `preset selectors` or custom selectors
- Doing `spatio-temporal cross validation` and writing them in machine learning friendly formats like `zarr`
- Providing en exhaustive set of `metrics` used with climate data or climate related hazards. 
](https://codecov.io/gh/ClimAI/climpy)

The package is divided into three parts
- The package has three modules
    - `transform`: It has a set of conditions forming a criterion which can be applied to any dataset. A subclass of criterion called hazard helps to create an event. Select class helps in selecting the events based on some rules. Lastly datasets can be linked to events. 
    - `ml_data`: The module helps to create X, Y pairs of machine learning dataset. It focuses on rigorous spatio-temporal cross validation and writing datasets in efficient dataset formats like zarr
    - `metrics`: The module provides an exhaustive list of metrics for spatio-temporal cross validation

Installation:
- The package requires `libgeos-dev`. On Debain(linux) it can be installed using the command `sudo apt -y install libgeos-dev`. On mac one can use `brew install geos` Cartopy has `libgeos-dev`  as a dependency. # More testing required.
- Then the package can be installed using `pip install climpy`