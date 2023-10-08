from abc import ABC;
from IHeatCapacityRatio import IHeatCapacityRatio;
from Errors.IterationErrors import IterationNotConverged
from typing import Dict, List


class IGasTank(ABC):
    """Class defining basic model of pressurized tank"""
    __Vector = list[float];
    def __init__(self,
                 initialPressure: float,  # [Pa]
                 tankInitialVolume: float,  # [m^3]
                 initialTemperature: float,  # [K]
                 initialMassOfGas: float,  # [kg]
                 specificGasConstant: float,  # [J/(kg*K)]
                 heatCapacityRatio: IHeatCapacityRatio  # [-]
                 ) -> None:
        self._pressureOfGas: float = initialPressure;
        self._volumeOfGas: float = tankInitialVolume;
        self._temperatureOfGas: float = initialTemperature;
        self._massOfGas: float = initialMassOfGas;
        self._specificGasConstant: float = specificGasConstant;
        self._heatCapacityRatio: IHeatCapacityRatio = heatCapacityRatio;
        self._densityOfGas: float = 0;
        self.calculateDensityOfGas();
        self._history: Dict[str, List[float]] = {
            "time": [],
            "pressure": [],
            "temperature": [],
            "mass": [],
            "density": []
        };

    def appendHistory(self, time: float) -> None:
        self._history["time"].append(time);
        self._history["pressure"].append(self._pressureOfGas);
        self._history["temperature"].append(self._temperatureOfGas);
        self._history["mass"].append(self._massOfGas);
        self._history["density"].append(self._densityOfGas);

    def incrementMassOfGas(self, massOfGasWhichIsMovedToTank: float) -> None:
        self._massOfGas += massOfGasWhichIsMovedToTank;

    def calculateDensityOfGas(self) -> None:
        if self._volumeOfGas == 0:
            self._densityOfGas = 0;
            return
        self._densityOfGas = self._massOfGas / self._volumeOfGas;

    def calculateTemperatureOfGas(self) -> None:
        max_number_of_iterations: int = 100;
        accepted_error: float = 1e-5;
        initial_temperature: float = self._temperatureOfGas;
        last_temperature: float = initial_temperature;
        error: float = accepted_error+1;

        if self._volumeOfGas == 0:
            return

        constant_pressure_part_stuff: float = (self._densityOfGas * self._specificGasConstant)/self._pressureOfGas;

        i: int = 0
        while i < max_number_of_iterations:
            heat_capacity_ratio: float = self._heatCapacityRatio.getHeatCapacityRatio(0.5 * (initial_temperature + self._temperatureOfGas));
            heat_ratio_part = (heat_capacity_ratio - 1)/heat_capacity_ratio;

            initial_temperature = self._temperatureOfGas * (constant_pressure_part_stuff * initial_temperature)**heat_ratio_part
            error = abs(initial_temperature - last_temperature);

            if error <= accepted_error:
                self._temperatureOfGas = initial_temperature;
                return

            last_temperature = initial_temperature
            i += 1;

        raise(IterationNotConverged(error, initial_temperature, i))

    def calculatePressureOfGas(self) -> None:
        self._pressureOfGas = self._densityOfGas * self._specificGasConstant * self._temperatureOfGas;

    def getPressure(self) -> float:
        return self._pressureOfGas;

    def getTemperature(self) -> float:
        return self._temperatureOfGas;

    def getDensity(self) -> float:
        return self._densityOfGas;

    def getHistory(self) -> Dict[str, List[float]]:
        return self._history
