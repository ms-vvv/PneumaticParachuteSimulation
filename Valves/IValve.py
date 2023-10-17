from abc import ABC, abstractmethod;
from typing import Dict, List
from IHistorable import IHistorable


class IValve(ABC, IHistorable):
    """Class defining basic model of valve between tanks"""

    def __init__(self) -> None:
        self._history: Dict[str, List[float]] = {
            "time": [],
            "massFlowRate": [],
        };
    @abstractmethod
    def getMaxMassFlowRate(self) -> float:
        pass;

    @abstractmethod
    def calculateMaxMassFlowRate(self) -> None:
        pass;

    @abstractmethod
    def appendHistory(self, time: float) -> None:
        pass

    @abstractmethod
    def getHistory(self) -> Dict[str, List[float]]:
        pass
