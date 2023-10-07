from IValve import IValve
from Cylinder import Cylinder
from Tank import Tank
from IHeatCapacityRatio import IHeatCapacityRatio;
from typing import Dict, List

class ValveWithCompressibleFlow(IValve):

    def __init__(self, minimalCrossSectionArea: float,  # [m^3]
                 tank: Tank,
                 cylinder: Cylinder,
                 heatCapacityRatio: IHeatCapacityRatio  # [-]
                 ) -> None:
        self._minimalCrossSectionArea: float = minimalCrossSectionArea;
        self._areaCorrectionFactor: float = 1;
        self._tank: Tank = tank;
        self._cylinder: Cylinder = cylinder;
        self._heatCapacityRatio: IHeatCapacityRatio = heatCapacityRatio;
        self._massFlowRate: float = 0;
        self._history: Dict[str, List[float]] = {
            "time": [],
            "massFlowRate": [],
        };

    def calculateMaxMassFlowRate(self) -> None:
        heat_capacity_ratio: float = self._heatCapacityRatio.getHeatCapacityRatio(
            0.5 * (self._tank.getTemperature() + self._cylinder.getTemperature()));

        heat_ratio_part = (heat_capacity_ratio - 1) / heat_capacity_ratio;
        pressure_ratio = self._cylinder.getPressure() / self._tank.getPressure()

        max_mass_flow_rate: float = (self._areaCorrectionFactor * self._minimalCrossSectionArea
                                    * pressure_ratio ** (1 / heat_capacity_ratio)
                                    * (2 * self._tank.getPressure() * (heat_ratio_part ** (-1)) * self._tank.getDensity()
                                       * (1 - pressure_ratio ** heat_ratio_part)
                                       ) ** 0.5);

        self._massFlowRate = max_mass_flow_rate

    def getMaxMassFlowRate(self) -> float:
        return self._massFlowRate

    def appendHistory(self, time: float) -> None:
        self._history["time"].append(time);
        self._history["massFlowRate"].append(self._massFlowRate);

    def getHistory(self) -> Dict[str, List[float]]:
        return self._history
