from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import xarray as xr
from climpy.transform.event import EventList
import numpy as np

################### Links ####################

"""
Links will always be associated with an event and can 
be applied to an xarray dataset to get some values 
corresponding to some events.
"""

class LinkData(ABC):
    def __init__(self) -> None:
        pass
    @abstractmethod
    def get_values(self):
        pass

    @abstractmethod
    def on_events(self):
        pass

class ValueAtTimeOffset(LinkData):
    def __init__(self, delta_t:timedelta) -> None:
        self.delta_t = delta_t

    def on_events(self, event_list: EventList):
        self.t_val = [event.tau + self.delta_t for event in event_list]

    def get_values(self, data:xr.DataArray):
        return [data.sel(time = t) for t in self.t_val]
        

class ValueOverTimeInterval(LinkData):
    def __init__(self, delta_t1, delta_t2=timedelta(0)) -> None:
        self.delta_t1 = delta_t1
        self.delta_t2 = delta_t2

    def on_events(self, event_list:EventList ):
        self.t_val = [slice(event.tau + self.delta_t1, event.tau + self.delta_t2) for event in event_list]

    def get_values(self, data):
        #! This could be limiting in the long run 
        return [data.sel(time = t) for t in self.t_val]