from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Union
from climpy.transform.event import EventList
import operator


############ EventSelector Definitions ##############

class EventSelector:
    def __init__(self, event_list: EventList) -> None:
        self.event_list = event_list

    def filter_by_rule(self, rule):
        event_index = rule.get_index(self.event_list)
        return self.event_list[event_index]

############ Arbitrary method to select between two events ##############

class BinaryEventSelector(ABC):
    pass

class SelectLargerEvent(BinaryEventSelector):
    def __init__(self, event_prev, event_next, attribute = "max_intensity") -> None:
        self.attribute = attribute

        attr_prev = getattr(event_prev, self.attribute)
        attr_next = getattr(event_next, self.attribute)
        
        
        if attr_prev > attr_next:
            self.keep_prev = True
            self.keep_next = False
        else:
            self.keep_prev = False
            self.keep_next = True

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

    def get_index(self, event_list:EventList, binary_event_selector = SelectLargerEvent):
        index_set = set()
        
        i = 0
        j = 1
        
        while j< len(event_list):
            event_prev = event_list[i]
            event_next = event_list[j]

            event_next_attr = getattr(event_next, self.attribute)
            event_prev_attr = getattr(event_prev, self.attribute)


            if self.comparision_operator(event_next_attr - event_prev_attr, self.threshold):
                index_set.add(i)
                i=j
                j=j+1
            else:
                be_selector = binary_event_selector(event_prev = event_prev, event_next=event_next)
                if be_selector.keep_prev:
                    j+=1
                elif be_selector.keep_next:
                    i=j
                    j+=1

        index_set.add(i)
        return list((sorted(index_set)))


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
        
    
