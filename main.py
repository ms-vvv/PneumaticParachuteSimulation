from Cylinder import Cylinder
from Tank import Tank
from ValveFactory import ValveFactory
from SimulationWithOneTankAndOnePiston import SimulationWithOneTankAndOnePiston
from HeatCapacityRatioFactory import HeatCapacityRatioFactory
import math as m
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


CO2_Tank_pressure = 70e5;  # [Pa]
CO2_Tank_mass = 88e-3;  # [kg]
CO2_Specific_gas_constant = 188.92;  # [J/(kg*K)]
CO2_Tank_temperature = 273.15 + 21;  # [K]

CO2_Tank_Volume = CO2_Tank_mass * CO2_Specific_gas_constant * CO2_Tank_temperature / CO2_Tank_pressure

heatCapacityRatioFactory = HeatCapacityRatioFactory()
CO2_Heat_capacity_ratio = heatCapacityRatioFactory.getCO2HeatCapacityRatio()

piston_Area = 0.25 * m.pi * (1e-2)**2;  # [m^3]
piston_Mass = 1;  # [kg]
piston_Length = 0.2;  # [m]

valve_Minimum_area = 0.25 * m.pi * (2e-3)**2;  # [m^3]


cylinder = Cylinder(CO2_Tank_pressure,
                    CO2_Tank_Volume,
                    CO2_Tank_temperature,
                    CO2_Tank_mass,
                    CO2_Specific_gas_constant,
                    CO2_Heat_capacity_ratio,
                    piston_Area,
                    piston_Mass,
                    piston_Length);

tank = Tank(CO2_Tank_pressure,
            CO2_Tank_Volume,
            CO2_Tank_temperature,
            CO2_Tank_mass,
            CO2_Specific_gas_constant,
            CO2_Heat_capacity_ratio)

valveFactory = ValveFactory()
valve = valveFactory.getValveWithCompressibleFlow(valve_Minimum_area,
                                                  tank,
                                                  cylinder,
                                                  CO2_Heat_capacity_ratio);


simulation = SimulationWithOneTankAndOnePiston(tank, cylinder, valve);

if __name__ == '__main__':
    simulation_End_time = 1.6;  # [s]
    simulation.runSimulation(simulation_End_time);

    #print(np.around(cylinder.getHistory()["time"], decimals=2))
    # print(np.transpose(np.array([cylinder.getHistory()["time"], cylinder.getHistory()["pistonPosition"], cylinder.getHistory()["pistonVelocity"], cylinder.getHistory()["pistonAcceleration"], cylinder.getHistory()["pressure"]])))
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Cone Position vs time", "Cone Velocity vs time", "Cone Acceleration vs time"))
    fig.add_trace(go.Scatter(x=cylinder.getHistory()["pistonPosition"], y=cylinder.getHistory()["time"],
                             mode='lines',
                             name='position'),
                             row=1, col=1)

    fig.add_trace(go.Scatter(x=cylinder.getHistory()["pistonVelocity"], y=cylinder.getHistory()["time"],
                             mode='lines',
                             name='velocity'),
                             row=2, col=1)

    fig.add_trace(go.Scatter(x=cylinder.getHistory()["pistonAcceleration"], y=cylinder.getHistory()["time"],
                             mode='lines',
                             name='acceleration'),
                             row=3, col=1)

    # Update xaxis properties
    fig.update_xaxes(title_text="Position [m]", row=1, col=1)
    fig.update_xaxes(title_text="Velocity [m/s]", row=2, col=1)
    fig.update_xaxes(title_text="Acceleration [m/s^2]", row=3, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="time [s]", range=[0, simulation_End_time])

    fig.show()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=cylinder.getHistory()["time"], y=np.array(cylinder.getHistory()["pressure"])*1e-5,
                             mode='lines',
                             name='cylinder'))

    fig2.add_trace(go.Scatter(x=tank.getHistory()["time"], y=np.array(tank.getHistory()["pressure"])*1e-5,
                             mode='lines',
                             name='tank', ))

    fig2.show()