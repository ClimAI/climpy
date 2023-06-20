from abc import ABC, abstractmethod
import numpy as np
from copy import deepcopy
from climpy.hazard.utils import reduce_datetime_precision
from datetime import timedelta
from typing import Union
import operator


############ Hazard Event Definitions #################

class HazardEvent(ABC):
    @abstractmethod
    def __repr__(self) -> str:
       pass

    def set_intensity(self):
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
        self.duration = self.end_time - self.start_time

        self.time_max_intensity = reduce_datetime_precision(self.data.time[self.data.argmax(dim="time")])
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

############ EventList Definitions #################


# * TODO Make all the classes iterable, this is required

class HazardEventList(ABC):
    pass

class PointHazardEventList(HazardEventList):
    def __init__(self, event_list: list[PointHazardEvent] ) -> None:
        self.event_list = event_list



class SpatialHazardEventList(HazardEventList):
    pass

class ArealHazardEventList(SpatialHazardEventList):
    pass

class VolumeHazardEventList(SpatialHazardEventList):
    pass

############ EventSelector Definitions ##############

class EventSelector:
    def __init__(self, event_list: HazardEventList) -> None:
        self.event_list = event_list.event_list

    def filter_by_rule(self, rule):
        arr_index = rule.get_index(self.event_list)
        
        return self.event_list[list(arr_index)]

############ Arbitrary method to select between two events ##############

class BinaryEventSelector(ABC):
    pass

class SelectLargerEvent(BinaryEventSelector):
    def __init__(self, event_prev, event_next, attribute = "max_intensity") -> None:
        self.attribute = attribute

        attr_prev = getattr(event_prev, self.attribute)
        attr_next = getattr(event_next, self.attribute)
        
        if attr_prev > attr_next:
            self.index_prev = 1
            self.index_next = 0
        else:
            self.index_prev = 0
            self.index_next = 1

class DropPreviousEvent(BinaryEventSelector):
    def __init__(self,):

        self.index_new = 0
        self.index_prev = 1
        

############ EventRule Definitions ##############

class Rule(ABC):
    pass

class SequentialRule(Rule):
    def __init__(self):
        pass

    def get_index(self, event_list:list, binary_event_selector = SelectLargerEvent):
        index_arr = np.zeros(len(event_list))
        self.pass_loop = False
        
        # Easy to understand implementation exist based on popping elements of a list
        # Getting index would still have a more convoluted logic

        for i, event in enumerate(event_list):
            if self.pass_loop:
                self.pass_loop == False
            else:
                if i<1:
                    index_arr[i] = 1
                    event_prev = event
                else:
                    event_next = event 
                    event_next_attr = getattr(event_next, self.attribute)
                    event_prev_attr = getattr(event_prev, self.attribute) 
                    if self.comparision_operator(event_next_attr - event_prev_attr,self.threshold):                    
                        index_arr[i] = 1
                        event_prev = event_next
                    else:
                        be_selector = binary_event_selector(event_prev = event_prev, event_next=event_next)
                        index_arr[i-1] = be_selector.index_prev
                        index_arr[i] = be_selector.index_next

                        event_prev = event_next

                        if be_selector.index_next == 0:
                            self.pass_loop = True
                        

        return index_arr.astype(int)


class TimeBetweenEvents(SequentialRule):
    def __init__(self, operator_str:str, delta_time:Union[timedelta, str], attribute = "time_max_intensity" ) -> None:
        
        self.threshold = delta_time
        self.attribute = attribute
        
        operators = {
        '>': operator.gt,
        '<': operator.lt
        }

        if operator_str in operators:
            comparision_operator = operators[operator_str]
            self.comparision_operator = comparision_operator
        else:
            raise ValueError(f"operator_str should be one of '>' or '<' instead of {operator_str}")
        
    
