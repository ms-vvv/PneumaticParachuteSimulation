from abc import ABC, abstractmethod;
from typing import Dict, List


class IHistorable():
    def __init__(self) -> None:
        self._history: Dict[str, List[float]] = {
            "time": [],
        };

    @abstractmethod
    def appendHistory(self, time: float) -> None:
        pass;

    def getHistory(self) -> Dict[str, List[float]]:
        return self._history
