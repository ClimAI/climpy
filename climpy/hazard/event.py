from abc import ABC, abstractmethod
import numpy as np
from copy import deepcopy
from climpy.hazard.utils import reduce_datetime_precision

############ Hazard Definitions #################

class Hazard(ABC):
    
    @abstractmethod
    def get_event(self):
        pass
    @abstractmethod
    def apply_criterion(self, x):
        pass

class PointHazard(Hazard):
    def __init__(self, criterion) -> None:
        
        self.sequence = criterion.sequence

    def apply_criterion(self, x):
        self.data = deepcopy(x)
        for condition in self.sequence:
            x = condition(x)
        
        self.location = x
        self.n_events = np.unique(x).shape[0]-1
    
    def get_event(self, event_index):
        event_index+=1 # Oth label is no event
        event_data = self.data.where(self.location==event_index, drop=True)
        event_location = self.location.where(self.location==event_index, drop=True)        

        return PointHazardEvent(event_data, event_location)


class SpatialHazard(Hazard):
    def __init__(self, criterion) -> None:
        
        self.sequence = criterion.sequence

    def apply_criteria(self, x):
        self.data = deepcopy(x)
        for condition in self.sequence:
            x = condition(x)
        
        self.location = x
        self.n_events = np.unique(x).shape[0]-1

class ArealHazard(SpatialHazard):
    def __init__(self, criterion) -> None:
        
        self.sequence = criterion.sequence

    def get_event(self, event_index):
        event_index+=1 # Oth label is no event
        event_data = self.data.where(self.location==event_index, drop=True)
        event_location = self.location.where(self.location==event_index, drop=True)        

        return ArealHazardEvent(event_data, event_location)

############ Hazard Event Definitions #################

class HazardEvent(ABC):
    @abstractmethod
    def __repr__(self) -> str:
       pass


class PointHazardEvent(HazardEvent):
    def __init__(self, event_data, event_location) -> None:
        
        self.hazard_event_type = "Areal Hazard Event"
        self.data = event_data
        self.location = event_location
        self.start_time = self.data.time[0].values
        self.end_time = self.location.time[-1].values

        self.max_intensity = self.data.max()
        self.total_intensity = self.data.sum()


    
    def __repr__(self) -> str:
        event_type = f"{self.hazard_event_type}:"

        temporal_extent = f"    * Temporal Extent: {reduce_datetime_precision(self.start_time)} to {reduce_datetime_precision(self.end_time)}" 
       
        return   "\n".join([event_type, temporal_extent])  
       
class SpatialHazardEvent(HazardEvent):
    def __repr__(self) -> str:
        
        event_type = f"{self.hazard_event_type}:"

        temporal_extent = f"    * Temporal Extent: {reduce_datetime_precision(self.start_time)} to {reduce_datetime_precision(self.end_time)}" 
        spatial_extent = f"    * Spatial Extent: Diagonally Opposite End Points(lon, lat) ({self.extent[0]} , {self.extent[1]})"
        
        return   "\n".join([event_type, temporal_extent, spatial_extent])  

class ArealHazardEvent(SpatialHazardEvent):
    def __init__(self, event_data, event_location) -> None:
        
        self.hazard_event_type = "Areal Hazard Event"
        self.data = event_data
        self.location = event_location
        self.start_time = self.data.time[0].values
        self.end_time = self.location.time[-1].values

        self.max_pixels_t = self.location.sum(dim =["lat", "lon"]).max()
        self.total_pixels = self.location.sum()

        self.max_intensity = self.data.max()
        self.total_intensity = self.data.sum()

        self.extent = (self.location.lon.min().item(), self.location.lat.max().item()), (self.location.lon.max().item(), self.location.lat.min().item())

class VolumeHazardEvent(SpatialHazardEvent):
    pass