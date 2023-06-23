from abc import ABC, abstractmethod
import numpy as np

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


class PercentBias():
    pass

class TimeSeriesMetrics(Metric):
    def __init__(self, y_true, y_pred) -> None:
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)

    @abstractmethod
    def calculate(self):
        pass
    def __call__(self):
        self.calculate()
class MeanAbsoluteError(TimeSeriesMetrics):
    def calculate(self):
        return np.mean(np.abs(self.y_true-self.y_pred))

class RootMeanSquaredError(TimeSeriesMetrics):
    def calculate(self):
        error = self.y_true - self.y_pred
        return np.sqrt(np.mean(np.square(error)))

class NormalizedRootMeanSquaredError(TimeSeriesMetrics):
    pass

class NashSutCliffeEfficiency(TimeSeriesMetrics):
    def calculate(self):
        numerator = np.sum(np.square(self.y_true - self.y_pred))
        denominator = np.sum(np.square(self.y_true - self.y_true.mean()))
        return 1 - numerator/denominator
    


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