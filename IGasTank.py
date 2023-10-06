from abc import ABC;
from IHeatCapacityRatio import IHeatCapacityRatio;
from Errors.IterationErrors import IterationNotConverged


class IGasTank(ABC):
    def __init__(self,
                 initialPressure: float,
                 tankInitialVolume: float,
                 initialTemperature: float,
                 initialMassOfGas: float,
                 specificGasConstant: float,
                 heatCapacityRatio: IHeatCapacityRatio) -> None:
        self._pressureOfGas: float = initialPressure;
        self._volumeOfGas: float = tankInitialVolume;
        self._temperatureOfGas: float = initialTemperature;
        self._massOfGas: float = initialMassOfGas;
        self._specificGasConstant: float = specificGasConstant;
        self._heatCapacityRatio: IHeatCapacityRatio = heatCapacityRatio;
        self._densityOfGas: float = 0;
        self.calculateDensityOfGas();

    def changeMassOfGasInTank(self, massOfGasWhichIsMovedToTank: float) -> None:
        self._massOfGas += massOfGasWhichIsMovedToTank;

    def calculateDensityOfGas(self) -> None:
        self._densityOfGas = self._massOfGas / self._volumeOfGas;

    def calculateTemperatureInsideTank(self) -> None:
        max_number_of_iterations: int = 100;
        accepted_error: float = 1e-5;
        initial_temperature: float = self._temperatureOfGas;
        error: float = accepted_error+1;

        constant_pressure_part_stuff: float = (self._densityOfGas * self._specificGasConstant)/self._pressureOfGas;

        i: int = 0
        while i < max_number_of_iterations:
            heat_capacity_ratio_ratio: float = self._heatCapacityRatio.getHeatCapacityRatio(0.5 * (initial_temperature + self._temperatureOfGas));
            heat_ratio_part = (heat_capacity_ratio_ratio - 1)/heat_capacity_ratio_ratio;

            initial_temperature = self._temperatureOfGas * (constant_pressure_part_stuff * initial_temperature)**heat_ratio_part
            error = abs(initial_temperature - self._temperatureOfGas);

            if error <= accepted_error:
                self._temperatureOfGas = initial_temperature;
                return

            i += 1;

        raise(IterationNotConverged(error, initial_temperature, i))

    def calculatePressureInsideTank(self) -> None:
        self._pressureOfGas = self._densityOfGas * self._specificGasConstant * self._temperatureOfGas;
