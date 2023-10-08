from abc import ABC, abstractmethod;


class IValve(ABC):
    """Class defining basic model of valve between tanks"""
    @abstractmethod
    def getMaxMassFlowRate(self) -> float:
        pass;


