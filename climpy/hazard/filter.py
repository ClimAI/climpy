from abc import ABC, abstractmethod

class EventFilter(ABC):
    pass

class PointEventFilter(ABC):
    def __init__(self, EventList) -> None:
        super().__init__()