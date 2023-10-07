from IForce import IForce
from IGasTank import IGasTank
from IHeatCapacityRatio import IHeatCapacityRatio;

class Cylinder(IGasTank):
    """Class representing part of the system with piston"""
    def __init__(self, initialPressure: float,
                 tankInitialVolume: float,
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
        self._isOutOfPiston: bool = False
        self._history = {
            "pistonPosition": [],
            "pistonVelocity": [],
            "pistonAcceleration": [],
        }

    def appendHistory(self, time: float) -> None:
        super().appendHistory(time)
        self._history["pistonPosition"].append(self._pistonPosition);
        self._history["pistonVelocity"].append(self._pistonVelocity);
        self._history["pistonAcceleration"].append(self._pistonAcceleration);

    def getPistonLength(self) -> float:
        return self._pistonLength;

    def getPistonPosition(self) -> float:
        return self._pistonPosition

    def pistonHasLeftTheCylinder(self) -> None:
        self._isOutOfPiston = True;

    def calculatePistonAcceleration(self, *forces: IForce) -> None:
        forces_acting_on_piston = self._pressureOfGas*self._pistonArea;
        for force in forces:
            if self._isOutOfPiston and force.isPistonForce():
                continue
            forces_acting_on_piston += force.getForce();

        self._pistonAcceleration = forces_acting_on_piston/self._pistonMass;

    