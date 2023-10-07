from abc import ABC, abstractmethod;
from ValveWithCompressibleFlow import ValveWithCompressibleFlow
from Cylinder import Cylinder
from Tank import Tank
from IHeatCapacityRatio import IHeatCapacityRatio;


class IValve(ABC):
    """Class defining basic model of valve between tanks"""
    @abstractmethod
    def getMaxMassFlowRate(self) -> float:
        pass;


class ValveFactory:

    def getValveWithCompressibleFlow(self, minimalCrossSectionArea: float,  # [m^3]
                                     tank: Tank,
                                     cylinder: Cylinder,
                                     heatCapacityRatio: IHeatCapacityRatio  # [-]
                                     ) -> ValveWithCompressibleFlow:
        return ValveWithCompressibleFlow(minimalCrossSectionArea,
                                         tank,
                                         cylinder,
                                         heatCapacityRatio)
