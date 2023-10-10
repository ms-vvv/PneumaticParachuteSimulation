from ISimulation import ISimulation
from Tanks.Cylinder import Cylinder
from Tanks.Tank import Tank
from Valves.ValveWithCompressibleFlow import ValveWithCompressibleFlow
from Forces.ForceFactory import ForceFactory
from Errors.IterationErrors import IterationNotConverged
import logging


class SimulationWithOneTankAndOnePiston(ISimulation):

    def __init__(self, tank: Tank, cylinder: Cylinder, valve: ValveWithCompressibleFlow):
        self._tank: Tank = tank;
        self._cylinder: Cylinder = cylinder;
        self._valve: ValveWithCompressibleFlow = valve;
        self._timeStep: float = 1e-6;  # [s]

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

        while time <= endTime and self._cylinder.getPistonLength() > self._cylinder.getPistonPosition():

            self._RK1_5(cylinder_history, time)

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

            self._tank.appendHistory(time)
            self._cylinder.appendHistory(time)
            self._valve.appendHistory(time)

            time += self._timeStep;

        # Piston now is pushed out of cylinder
        self._timeStep = 1e-2
        self._cylinder.setPressureToZero();

        while time <= endTime:
            self._RK1_5(cylinder_history, time)
            # Calculating acceleration of the piston
            drag_force.setVelocity(rocket_speed_at_deployment + self._cylinder.getPistonVelocity())
            self._cylinder.calculatePistonAcceleration(drag_force)

            self._tank.appendHistory(time)
            self._cylinder.appendHistory(time)
            self._valve.appendHistory(time)

            time += self._timeStep;
