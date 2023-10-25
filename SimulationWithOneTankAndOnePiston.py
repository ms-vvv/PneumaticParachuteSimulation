from ISimulation import ISimulation
from Tanks.Cylinder import Cylinder
from Tanks.Tank import Tank
from Valves.ValveWithCompressibleFlow import ValveWithCompressibleFlow
from Forces.ForceFactory import ForceFactory
from Errors.IterationErrors import IterationNotConverged
import logging
from Forces.DragForces import SimpleDragForce


class SimulationWithOneTankAndOnePiston(ISimulation):

    def __init__(self,
                 tank: Tank,
                 cylinder: Cylinder,
                 valve: ValveWithCompressibleFlow,
                 dragForceForSimulationInCylinder: SimpleDragForce,
                 dragForceForSimulationOutOfCylinder: SimpleDragForce) -> None:
        self._tank: Tank = tank;
        self._cylinder: Cylinder = cylinder;
        self._valve: ValveWithCompressibleFlow = valve;
        self._timeStep: float = 1e-7;  # [s]
        self._dragForceForSimulationInCylinder: SimpleDragForce = dragForceForSimulationInCylinder;
        self._dragForceForSimulationOutOfCylinder: SimpleDragForce = dragForceForSimulationOutOfCylinder;
        self._referenceSpeed: float = 0;
        self._time: float = 0;

    def setReferenceSpeed(self, referenceSpeed: float) -> None:
        self._referenceSpeed = referenceSpeed;

    def _RK1_5(self, cylinder_history: dict[str, list[float]], time: float) -> None:
        time_step: float = time - cylinder_history["time"][-1]
        previous_time_step: float = (cylinder_history["time"][-1] - cylinder_history["time"][-2])
        # Piston velocity
        self._cylinder.incrementPistonVelocity(
            0.5 * (
                    (1
                            #(time_step / previous_time_step) *
                           # (cylinder_history["pistonAcceleration"][-1] - cylinder_history["pistonAcceleration"][-2])
                    ) + 2 * cylinder_history["pistonAcceleration"][-1]
                   ) * time_step);
        # Piston movement
        self._cylinder.incrementPistonPosition(
            0.5 * (self._cylinder.getPistonVelocity() + cylinder_history["pistonVelocity"][-1]) * time_step);

    def _initializeSimulationCalculations(self, startTime: float = 0) -> None:

        self._time = startTime

        # Zero time step
        self._tank.appendHistory(self._time)
        self._cylinder.appendHistory(self._time)
        self._valve.appendHistory(self._time)

        self._time += self._timeStep / 2

        # 0.5 time step
        self._tank.appendHistory(self._time)
        self._cylinder.appendHistory(self._time)
        self._valve.appendHistory(self._time)

        self._time += self._timeStep;

    def _simulationCalculationsWithPistonInCylinder(self, endTime: float, startTime: float = 0) -> None:

        self._cylinder.calculatePistonAcceleration(self._dragForceForSimulationInCylinder)

        self._time = startTime

        cylinder_history = self._cylinder.getHistory();
        valve_history = self._valve.getHistory()

        while self._time <= endTime and self._cylinder.getPistonLength() > self._cylinder.getPistonPosition():

            self._RK1_5(cylinder_history, self._time)

            # New volume after piston moved
            self._cylinder.calculateVolume();

            # Calculating density of the gas in tank and cylinder
            self._cylinder.calculateDensityOfGas()
            self._tank.calculateDensityOfGas()

            # Calculate temperature of the gas in tank and cylinder
            try:
                self._cylinder.calculateTemperatureOfGas()
                self._tank.calculateTemperatureOfGas()
            except IterationNotConverged:
                logging.exception(f"interation of temperature on {self._time}s")
                return

            # Calculate pressure of the gas in tank and cylinder
            self._cylinder.calculatePressureOfGas()
            self._tank.calculatePressureOfGas()

            # Calculating mass flow rate through the valve
            self._valve.calculateMaxMassFlowRate()

            # Incrementing mass of the gas in tank and cylinder
            mass_displacement: float = 0.5 * (
                        self._valve.getMaxMassFlowRate() + valve_history["massFlowRate"][-1]) * self._timeStep
            self._cylinder.incrementMassOfGas(mass_displacement);
            self._tank.incrementMassOfGas(-mass_displacement);

            # Calculating acceleration of the piston
            self._dragForceForSimulationInCylinder.setVelocity(self._referenceSpeed + self._cylinder.getPistonVelocity())
            self._cylinder.calculatePistonAcceleration(self._dragForceForSimulationInCylinder)

            self._tank.appendHistory(self._time)
            self._cylinder.appendHistory(self._time)
            self._valve.appendHistory(self._time)

            self._time += self._timeStep;

    def _simulationCalculationsWithPistonOutOffCylinder(self, endTime: float, startTime: float = 0) -> None:
        cylinder_history = self._cylinder.getHistory();
        # valve_history = self._valve.getHistory()

        self._time = startTime

        while self._time <= endTime:
            self._RK1_5(cylinder_history, self._time)
            # Calculating acceleration of the piston
            self._dragForceForSimulationOutOfCylinder.setVelocity(self._referenceSpeed + self._cylinder.getPistonVelocity())
            self._cylinder.calculatePistonAcceleration(self._dragForceForSimulationOutOfCylinder)

            # self._tank.appendHistory(time)
            self._cylinder.appendHistory(self._time)
            # self._valve.appendHistory(time)

            self._time += self._timeStep;


    def runSimulation(self, endTime: float, startTime: float = 0) -> None:

        self._initializeSimulationCalculations(startTime)

        self._simulationCalculationsWithPistonInCylinder(endTime, startTime);

        # Piston now is pushed out of cylinder
        self._timeStep = 1e-2;
        self._cylinder.setPressureToZero();

        self._simulationCalculationsWithPistonOutOffCylinder(endTime, self._time)


