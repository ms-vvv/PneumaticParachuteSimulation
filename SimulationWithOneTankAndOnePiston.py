from ISimulation import ISimulation
from Cylinder import Cylinder
from Tank import Tank
from ValveWithCompressibleFlow import ValveWithCompressibleFlow


class SimulationWithOneTankAndOnePiston(ISimulation):

    def __init__(self, tank: Tank, cylinder: Cylinder, valve: ValveWithCompressibleFlow):
        self._tank: Tank = tank;
        self._cylinder: Cylinder = cylinder;
        self._valve: ValveWithCompressibleFlow = valve;
        self._timeStep: float = 1e-3;  # [s]


    def runSimulation(self, endTime: float, startTime: float = 0) -> None:
        time: float = self._timeStep;


        while time < endTime or self._cylinder.getPistonLength() < self._cylinder.getPistonPosition():

            time += self._timeStep;

        self._cylinder.pistonHasLeftTheCylinder();
        self._timeStep = 1e-2

        while time < endTime:

            time += self._timeStep;