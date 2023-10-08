from abc import ABC, abstractmethod


class IForce(ABC):

    @abstractmethod
    def getForce(self) -> float:
        pass;

    @abstractmethod
    def isPistonForce(self) -> bool:
        pass;

