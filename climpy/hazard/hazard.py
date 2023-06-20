from abc import ABC, abstractmethod
from copy import deepcopy
import numpy as np

from climpy.hazard.event import (PointHazardEvent, 
                                 ArealHazardEvent, 
                                 VolumeHazardEvent,
                                 PointHazardEventList,
                                 ArealHazardEventList,
                                 VolumeHazardEventList)


class Hazard(ABC):
    
    @abstractmethod
    def get_event(self):
        pass
    @abstractmethod
    def apply_criterion(self):
        pass
    @abstractmethod
    def all_events(self):
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

    def all_events(self):
        return PointHazardEventList([self.get_event(i) for i in range(self.n_events)])

class SpatialHazard(Hazard):
    def __init__(self, criterion) -> None:
        
        self.sequence = criterion.sequence

    def apply_criterion(self, x):
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
    
    def all_events(self,):
        return ArealHazardEventList([self.get_event(i+1) for i in range(self.n_events)])