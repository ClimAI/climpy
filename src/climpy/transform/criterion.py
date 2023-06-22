from abc import ABC, abstractmethod
from copy import deepcopy

class Criterion(ABC):

    def apply_conditions(self, x):
        self.data = deepcopy(x)
        for condition in self.sequence:
            x = condition(x)
        return x

    def valid_conditions(self):
        assert self.sequence[-1].return_binary == True
    

class PointCriterion(Criterion):
    def __init__(self, sequence:list) -> None:
        self.sequence = sequence


class SpatialCriterion(Criterion):
    def __init__(self, sequence:list) -> None:
        self.sequence = sequence
        
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True

class ArialCriterion(SpatialCriterion):
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True

class VolumenCriterion(SpatialCriterion):
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True

