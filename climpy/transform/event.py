from abc import ABC, abstractmethod
import numpy as np
from copy import deepcopy
from climpy.transform.utils import reduce_datetime_precision
from datetime import timedelta
from typing import Union, List
import operator


############  Event Definitions #################

class Event(ABC):
    """
    Every event should have a well defined tau and r. They may be overwritten but should have a minimum 
    """
    @abstractmethod
    def __repr__(self) -> str:
       pass

    def set_intensity(self):
        pass
        

class PointEvent(Event):
    def __init__(self, event_data, event_location) -> None:
        
        self.event_type = "Areal  Event"
        self.data = event_data
        self.location = event_location
        self.start_time = self.data.time[0].values
        self.end_time = self.location.time[-1].values
        self.max_intensity = self.data.max()
        self.total_intensity = self.data.sum()
        self.duration = self.end_time - self.start_time
        self.time_max_intensity = reduce_datetime_precision(self.data.time[self.data.argmax(dim="time")])
        self.tau = self.time_max_intensity

    def __repr__(self) -> str:
        event_type = f"{self.event_type}:"

        temporal_extent = f"    * Temporal Extent: {reduce_datetime_precision(self.start_time)} to {reduce_datetime_precision(self.end_time)}" 
       
        return   "\n".join([event_type, temporal_extent])  

class SpatialEvent(Event):
    def __repr__(self) -> str:
        
        event_type = f"{self.event_type}:"

        temporal_extent = f"    * Temporal Extent: {reduce_datetime_precision(self.start_time)} to {reduce_datetime_precision(self.end_time)}" 
        spatial_extent = f"    * Spatial Extent: Diagonally Opposite End Points(lon, lat) ({self.extent[0]} , {self.extent[1]})"
        
        return   "\n".join([event_type, temporal_extent, spatial_extent])  

class ArealEvent(SpatialEvent):
    def __init__(self, event_data, event_location) -> None:
        
        self.event_type = "Areal  Event"
        self.data = event_data
        self.location = event_location
        self.start_time = self.data.time[0].values
        self.end_time = self.location.time[-1].values

        self.max_pixels_t = self.location.sum(dim =["lat", "lon"]).max()
        self.total_pixels = self.location.sum()

        self.max_intensity = self.data.max()
        self.total_intensity = self.data.sum()

        self.extent = (self.location.lon.min().item(), self.location.lat.max().item()), (self.location.lon.max().item(), self.location.lat.min().item())

class VolumeEvent(SpatialEvent):
    pass

############ EventList Definitions #################


# * TODO Make all the classes iterable, this is required

class EventList(ABC):

    def __iter__(self):
        return iter(self.event_list)

class PointEventList(EventList):
    def __init__(self, event_list: List[PointEvent] ) -> None:
        self.event_list = event_list

    def __iter__(self):
        return iter(self.event_list)

    def __len__(self):
        return len(self.event_list)
    
    def __getitem__(self, idx):

        if isinstance(idx, list):
            return PointEventList([self.event_list[i] for i in idx])
        elif isinstance(idx, int):
            return self.event_list[idx]
        else:
            raise TypeError(f"Index is of type {type(idx)} instead of a list or an int")    

class SpatialEventList(EventList):
    pass

class ArealEventList(SpatialEventList):
    pass

class VolumeEventList(SpatialEventList):
    pass
