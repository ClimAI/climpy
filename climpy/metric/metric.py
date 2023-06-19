from abc import ABC, abstractmethod

class Metric(ABC):
    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def top_q():
        pass

    @abstractmethod
    def bottom_q():
        pass

    def __call__(self):
        return self.result()
    
class TimeSeriesMetrics(Metric):
    def __init__(self, y_true, y_pred) -> None:
        self.y_true = y_true
        self.y_pred = y_pred

class MeanAbsoluteError(TimeSeriesMetrics):
    pass

class RootMeanSquaredError(TimeSeriesMetrics):
    pass

class NormalizedRootMeanSquaredError(TimeSeriesMetrics):
    pass

class NashSutCliffeEfficiency(TimeSeriesMetrics):
    pass

class CoefficientOfDetermination(TimeSeriesMetrics):
    pass

class PercentBias(TimeSeriesMetrics):
    pass

class KlingGuptaEfficiency(TimeSeriesMetrics):
    pass

class IndexOfAgreement(TimeSeriesMetrics):
    pass

class RelativeVolumeError(TimeSeriesMetrics):
    pass

class KlingGuptaSkillScore(TimeSeriesMetrics):
    pass

class StandardDeviationRatio(TimeSeriesMetrics):
    pass

class ContinuityRatio(TimeSeriesMetrics):
    pass

class FlowDurationCurve(TimeSeriesMetrics):
    pass

class FrequencyBiasIndex(TimeSeriesMetrics):
    pass