from abc import ABC, abstractmethod

class ISimulation(ABC):

    @abstractmethod
    def runSimulation(self, endTime: float, startTime: float = 0) -> None:
        pass;
