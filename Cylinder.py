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

    def calculatePistonAcceleration(self, *forces: IForce) -> None:
        forces_acting_on_piston = self._pressureOfGas*self._pistonArea;
        for force in forces:
            forces_acting_on_piston += force.getForce();

        self._pistonAcceleration = forces_acting_on_piston/self._pistonMass;

    