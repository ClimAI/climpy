from abc import ABC, abstractmethod
from copy import deepcopy

from typing import List

import numpy as np

from climpy.transform.event import (PointEvent, 
                                 ArealEvent, 
                                 VolumeEvent,
                                 PointEventList,
                                 ArealEventList,
                                 VolumeEventList)

from climpy.transform.criterion import Criterion
from climpy.transform.condition import Condition

class Hazard(Criterion):
    
    @abstractmethod
    def get_event(self):
        pass

    @abstractmethod
    def all_events(self):
        pass

class PointHazard(Hazard):
    def __init__(self, condition_sequence = List[Condition]) -> None:
        
        self.sequence = condition_sequence

    def apply_conditions(self, x):
        self.data = deepcopy(x)
        for condition in self.sequence:
            x = condition(x)
        
        self.location = x
        self.n_events = np.unique(x).shape[0]-1
    
    def get_event(self, event_index):
        event_index+=1 # Oth label is no event
        event_data = self.data.where(self.location==event_index, drop=True)
        event_location = self.location.where(self.location==event_index, drop=True)        

        return PointEvent(event_data, event_location)

    def all_events(self):
        return PointEventList([self.get_event(i) for i in range(self.n_events)])
    

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

        return ArealEvent(event_data, event_location)
    
    def all_events(self,):
        return ArealEventList([self.get_event(i+1) for i in range(self.n_events)])