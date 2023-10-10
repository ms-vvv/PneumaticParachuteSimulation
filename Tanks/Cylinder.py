from Forces.IForce import IForce
from IGasTank import IGasTank
from Constants.IHeatCapacityRatio import IHeatCapacityRatio;

class Cylinder(IGasTank):
    """Class representing part of the system with piston"""
    def __init__(self, initialPressure: float,
                 tankInitialVolume: float,  # Volume at zero position
                 initialTemperature: float,
                 initialMassOfGas: float,
                 specificGasConstant: float,
                 heatCapacityRatio: IHeatCapacityRatio,
                 pistonArea: float,
                 pistonMass: float,
                 pistonLength: float,
                 initialPistonVelocity: float = 0,
                 initialPistonPosition: float = 0) -> None:
        super().__init__(initialPressure,
                         tankInitialVolume,
                         initialTemperature,
                         initialMassOfGas,
                         specificGasConstant,
                         heatCapacityRatio)
        self._pistonPosition: float = initialPistonPosition;
        self._pistonArea: float = pistonArea;
        self._pistonMass: float = pistonMass;
        self._pistonAcceleration: float = 0;
        self._pistonVelocity: float = initialPistonVelocity
        self._pistonLength: float = pistonLength
        self._tankInitialVolume: float = tankInitialVolume
        self._history.update({
            "pistonPosition": [],
            "pistonVelocity": [],
            "pistonAcceleration": [],
        })

    def appendHistory(self, time: float) -> None:
        super().appendHistory(time)
        self._history["pistonPosition"].append(self._pistonPosition);
        self._history["pistonVelocity"].append(self._pistonVelocity);
        self._history["pistonAcceleration"].append(self._pistonAcceleration);

    def getPistonLength(self) -> float:
        return self._pistonLength;

    def getPistonPosition(self) -> float:
        return self._pistonPosition

    def getPistonVelocity(self) -> float:
        return self._pistonVelocity

    def calculateVolume(self) -> None:
        self._volumeOfGas = self._tankInitialVolume + self._pistonArea * self._pistonPosition

    def calculatePistonAcceleration(self, *forces: IForce) -> None:
        forces_acting_on_piston = self._pressureOfGas*self._pistonArea;
        for force in forces:
            forces_acting_on_piston += force.getForce();

        self._pistonAcceleration = forces_acting_on_piston/self._pistonMass;

    def incrementPistonVelocity(self, VelocityIncrement: float) -> None:
        self._pistonVelocity += VelocityIncrement;

    def incrementPistonPosition(self, PositionIncrement: float) -> None:
        self._pistonPosition += PositionIncrement;

    def setPressureToZero(self) -> None:
        self._pressureOfGas = 0;
