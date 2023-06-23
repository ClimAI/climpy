from climpy.transform.criterion import ArialHazardCriterion
from climpy.transform.condition import ThresholdPercentile, ConnectStructure

import numpy as np


class FloodHazardCriterion(ArialHazardCriterion):
    def __init__(
        self,
        peak_threshold=0.95,
        connect_structure=np.array(
            [
                [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
                [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
                [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
            ]
        ),
    ):
        # Exact overlap in time and Exact + Diagonal overlap in space

        self.cond_1 = ThresholdPercentile(">", peak_threshold)
        self.cond_2 = ConnectStructure(connect_structure)
        self.sequence = [self.cond_1, self.cond_2]
