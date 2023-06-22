"""
Defines climpy.data which inherits from xarray.DataArray
"""
from abc import abstractmethod
from xarray import DataArray


class AbstractImpactData():
    
    @abstractmethod
    def find_events(self):
        pass
