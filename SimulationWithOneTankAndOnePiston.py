from ISimulation import ISimulation
from Cylinder import Cylinder
from Tank import Tank
from ValveWithCompressibleFlow import ValveWithCompressibleFlow
from IForce import ForceFactory
from Errors.IterationErrors import IterationNotConverged
import logging


class SimulationWithOneTankAndOnePiston(ISimulation):

    def __init__(self, tank: Tank, cylinder: Cylinder, valve: ValveWithCompressibleFlow):
        self._tank: Tank = tank;
        self._cylinder: Cylinder = cylinder;
        self._valve: ValveWithCompressibleFlow = valve;
        self._timeStep: float = 1e-3;  # [s]

    def RK1_5(self, cylinder_history: dict[str, list[float]]) -> None:
        # Piston velocity
        self._cylinder.incrementPistonVelocity(
            0.5 * ((((self._timeStep) / (cylinder_history["time"][-1] - cylinder_history["time"][-2])) *
                    (cylinder_history["pistonAcceleration"][-1] - cylinder_history["pistonAcceleration"][-2])) +
                   cylinder_history["pistonAcceleration"][-1]) * self._timeStep);
        # Piston movement
        self._cylinder.incrementPistonPosition(
            0.5 * (self._cylinder.getPistonVelocity() + cylinder_history["pistonVelocity"][-1]) * self._timeStep);

    def runSimulation(self, endTime: float, startTime: float = 0) -> None:

        force_factory = ForceFactory();
        # Drag force stuff
        drag_coefficient: float = 0.27951877;  # [-]
        cone_frontal_area: float = 0.017671459;  # [m^2]
        rocket_speed_at_deployment: float = 101.9180272;  # [m/s]
        air_density_at_deployment: float = 0.757121481;  # [kg/m^3]
        drag_force = force_factory.getSimpleDragForce(drag_coefficient, cone_frontal_area)
        drag_force.setAirDensity(air_density_at_deployment);
        drag_force.setVelocity(rocket_speed_at_deployment)

        self._cylinder.calculatePistonAcceleration(drag_force)

        # Zero time step
        self._tank.appendHistory(0)
        self._cylinder.appendHistory(0)
        self._valve.appendHistory(0)

        # 0.5 time step
        self._tank.appendHistory(self._timeStep/2)
        self._cylinder.appendHistory(self._timeStep/2)
        self._valve.appendHistory(self._timeStep/2)

        time: float = self._timeStep;

        cylinder_history = self._cylinder.getHistory();
        valve_history = self._valve.getHistory()

        while time < endTime or self._cylinder.getPistonLength() < self._cylinder.getPistonPosition():

            self.RK1_5(cylinder_history)

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
                logging.exception(f"interation of temperature on {time}s")
                return

            # Calculate pressure of the gas in tank and cylinder
            self._cylinder.calculatePressureOfGas()
            self._tank.calculatePressureOfGas()

            # Calculating mass flow rate through the valve
            self._valve.calculateMaxMassFlowRate()

            # Incrementing mass of the gas in tank and cylinder
            mass_displacement: float = 0.5 * (self._valve.getMaxMassFlowRate() + valve_history["massFlowRate"][-1]) * self._timeStep
            self._cylinder.incrementMassOfGas(mass_displacement);
            self._tank.incrementMassOfGas(-mass_displacement);
            
            # Calculating acceleration of the piston
            drag_force.setVelocity(rocket_speed_at_deployment + self._cylinder.getPistonVelocity())
            self._cylinder.calculatePistonAcceleration(drag_force)

            time += self._timeStep;

        self._timeStep = 1e-2
        self._cylinder.setPressureToZero();

        while time < endTime:
            self.RK1_5(cylinder_history)
            # Calculating acceleration of the piston
            drag_force.setVelocity(rocket_speed_at_deployment + self._cylinder.getPistonVelocity())
            self._cylinder.calculatePistonAcceleration(drag_force)

            time += self._timeStep;
