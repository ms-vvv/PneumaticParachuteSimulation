from Tanks.Cylinder import Cylinder
from Constants.IHeatCapacityRatio import IHeatCapacityRatio;
from Tank import Tank;


class GasTankFactory:
    def getTank(self, initialPressure: float,
                tankInitialVolume: float,
                initialTemperature: float,
                initialMassOfGas: float,
                specificGasConstant: float,
                heatCapacityRatio: IHeatCapacityRatio) -> Tank:

        return Tank(initialPressure,
                    tankInitialVolume,
                    initialTemperature,
                    initialMassOfGas,
                    specificGasConstant,
                    heatCapacityRatio);

    def getCylinder(self, initialPressure: float,
                         tankInitialVolume: float,
                         initialTemperature: float,
                         initialMassOfGas: float,
                         specificGasConstant: float,
                         heatCapacityRatio: IHeatCapacityRatio,
                         pistonArea: float,
                         pistonMass: float,
                         pistonLength: float) -> Cylinder:

        return Cylinder(initialPressure,
                         tankInitialVolume,
                         initialTemperature,
                         initialMassOfGas,
                         specificGasConstant,
                         heatCapacityRatio,
                         pistonArea,
                         pistonMass,
                         pistonLength);
