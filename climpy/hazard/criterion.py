from abc import ABC, abstractmethod

class HazardCriterion(ABC):
    @abstractmethod
    def valid_criterion(self):
        pass
    

class PointHazardCriterion(HazardCriterion):
    def __init__(self, sequence:list) -> None:
        self.sequence = sequence
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True


class SpatialHazardCriterion(HazardCriterion):
    def __init__(self, sequence:list) -> None:
        self.sequence = sequence
        
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True

class ArialHazardCriterion(SpatialHazardCriterion):
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True

class VolumenHazardCriterion(SpatialHazardCriterion):
    def valid_criterion(self):
        assert self.sequence[-1].return_binary == True

