from abc import ABC, abstractmethod
from DragForces import SimpleDragForce

class IForce(ABC):

    @abstractmethod
    def getForce(self) -> float:
        pass;

    @abstractmethod
    def isPistonForce(self) -> bool:
        pass;


class ForceFactory:

    def getSimpleDragForce(self, dragCoefficient: float, referenceArea: float) -> SimpleDragForce:
        return SimpleDragForce(dragCoefficient, referenceArea);
