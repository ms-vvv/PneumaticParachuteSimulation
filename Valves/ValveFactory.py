from ValveWithCompressibleFlow import ValveWithCompressibleFlow
from Tanks.Cylinder import Cylinder
from Tanks.Tank import Tank
from Constants.IHeatCapacityRatio import IHeatCapacityRatio;


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
