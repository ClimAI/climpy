"""
Defines climpy.data which inherits from xarray.DataArray
"""
from abc import abstractmethod


class AbstractImpactData:
    @abstractmethod
    def find_events(self):
        pass
