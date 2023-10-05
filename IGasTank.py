from abc import ABC, abstractmethod;


class IGasTank(ABC):
    def __init__(self, initialPressure: float, tankInitialVolume: float, initialTemperature: float, initaialMassOfGas: float) -> None:
        self._pressureOfGas: float = initialPressure;
        self._volumeOfGas: float = tankInitialVolume;
        self._temperatureOfGas: float = initialTemperature;
        self._massOfGas: float = initaialMassOfGas;
        self._densityOfGas: float;
        self.calculateDensityOfGas();


    @abstractmethod
    def calculatePressure(self) -> None:
        pass;

    def calculateDensityOfGas(self) -> None:
        self._densityOfGas = self._massOfGas / self._volumeOfGas;


