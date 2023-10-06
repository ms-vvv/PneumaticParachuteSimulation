from abc import ABC, abstractmethod;

class IHeatCapacityRatio(ABC):

    @abstractmethod
    def getHeatCapacityRatio(self, temperature: float) -> float:
        pass;

