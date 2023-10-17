from Forces.ForceFactory import ForceFactory
from Tanks.Cylinder import Cylinder
from Tanks.Tank import Tank
from Valves.ValveFactory import ValveFactory
from SimulationWithOneTankAndOnePiston import SimulationWithOneTankAndOnePiston
from Constants.HeatCapacityRatioFactory import HeatCapacityRatioFactory
import math as m
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# ---------CO2 tank properties---------
CO2_Tank_pressure = 70e5;  # [Pa]
CO2_Tank_mass = 88e-3;  # [kg]
CO2_Specific_gas_constant = 188.92;  # [J/(kg*K)]
CO2_Tank_temperature = 273.15 + 21;  # [K]

CO2_Tank_Volume = CO2_Tank_mass * CO2_Specific_gas_constant * CO2_Tank_temperature / CO2_Tank_pressure

# ---------CO2 properties---------
heatCapacityRatioFactory = HeatCapacityRatioFactory()
CO2_Heat_capacity_ratio = heatCapacityRatioFactory.getCO2HeatCapacityRatio()

# ---------Piston properties---------
piston_Area = 0.25 * m.pi * (2e-2)**2;  # [m^3]
piston_Mass = 1;  # [kg]
piston_Length = 0.2;  # [m]

# ---------Valve properties---------
valve_Minimum_area = 0.25 * m.pi * (5e-3)**2;  # [m^3]

# ---------Tanks initialization---------
cylinder = Cylinder(CO2_Tank_pressure,
                    CO2_Tank_Volume*0.01,
                    CO2_Tank_temperature,
                    CO2_Tank_mass*0.01,
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



# ---------Forces---------
force_factory = ForceFactory();

# Drag force stuff
drag_coefficient: float = 0.27951877;  # [-]
cone_frontal_area: float = 0.017671459;  # [m^2]
rocket_speed_at_deployment: float = 101.9180272;  # [m/s]
air_density_at_deployment: float = 0.757121481;  # [kg/m^3]

drag_force = force_factory.getSimpleDragForce(drag_coefficient, cone_frontal_area)
drag_force.setAirDensity(air_density_at_deployment);
drag_force.setVelocity(rocket_speed_at_deployment)


simulation = SimulationWithOneTankAndOnePiston(tank, cylinder, valve, drag_force, drag_force);

simulation.setReferenceSpeed(rocket_speed_at_deployment)

if __name__ == '__main__':
    simulation_End_time = 1.6;  # [s]
    simulation.runSimulation(simulation_End_time);

    # Movement plots
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Cone Position vs time", "Cone Velocity vs time", "Cone Acceleration vs time"))
    fig.add_trace(go.Scatter(x=cylinder.getHistory()["pistonPosition"], y=cylinder.getHistory()["time"],
                             mode='lines',
                             name='position'),
                             row=1, col=1)

    fig.add_trace(go.Scatter(x=cylinder.getHistory()["pistonVelocity"], y=cylinder.getHistory()["time"],
                             mode='lines',
                             name='velocity'),
                             row=2, col=1)

    fig.add_trace(go.Scatter(x=np.array(cylinder.getHistory()["pistonAcceleration"])/9.81, y=cylinder.getHistory()["time"],
                             mode='lines',
                             name='acceleration'),
                             row=3, col=1)

    # Update xaxis properties
    fig.update_xaxes(title_text="Position [m]", row=1, col=1)
    fig.update_xaxes(title_text="Velocity [m/s]", row=2, col=1)
    fig.update_xaxes(title_text="Acceleration [G]", row=3, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="time [s]", range=[0, simulation_End_time])

    fig.update_layout(width=700)

# Fluid properties plots
    fig2 = make_subplots(rows=2, cols=2, subplot_titles=("Pressure in system vs time", "Temperature in system vs time", "Density in system vs time", "Mass in system vs time"))

    # Pressure
    fig2.add_trace(go.Scatter(x=cylinder.getHistory()["time"], y=np.array(cylinder.getHistory()["pressure"])*1e-5,
                             mode='lines',
                             name='piston'),
                             row=1, col=1)

    fig2.add_trace(go.Scatter(x=tank.getHistory()["time"], y=np.array(tank.getHistory()["pressure"])*1e-5,
                             mode='lines',
                             name='tank', ),
                             row=1, col=1)

    # Temperature
    fig2.add_trace(go.Scatter(x=cylinder.getHistory()["time"], y=cylinder.getHistory()["temperature"],
                              mode='lines',
                              name='piston',
                              line_color=px.colors.qualitative.Plotly[0],
                              showlegend=False),
                   row=1, col=2)

    fig2.add_trace(go.Scatter(x=tank.getHistory()["time"], y=tank.getHistory()["temperature"],
                              mode='lines',
                              name='tank',
                              line_color=px.colors.qualitative.Plotly[1],
                              showlegend=False),
                   row=1, col=2)

    # Density
    fig2.add_trace(go.Scatter(x=cylinder.getHistory()["time"], y=cylinder.getHistory()["density"],
                              mode='lines',
                              name='piston',
                              line_color=px.colors.qualitative.Plotly[0],
                              showlegend=False),
                   row=2, col=1)

    fig2.add_trace(go.Scatter(x=tank.getHistory()["time"], y=tank.getHistory()["density"],
                              mode='lines',
                              name='tank',
                              line_color=px.colors.qualitative.Plotly[1],
                              showlegend=False),
                   row=2, col=1)

    # Mass
    fig2.add_trace(go.Scatter(x=cylinder.getHistory()["time"], y=np.array(cylinder.getHistory()["mass"])*1000,
                              mode='lines',
                              name='piston',
                              line_color=px.colors.qualitative.Plotly[0],
                              showlegend=False),
                   row=2, col=2)

    fig2.add_trace(go.Scatter(x=tank.getHistory()["time"], y=np.array(tank.getHistory()["mass"])*1000,
                              mode='lines',
                              name='tank',
                              line_color=px.colors.qualitative.Plotly[1],
                              showlegend=False),
                   row=2, col=2)

    fig2.add_trace(go.Scatter(x=valve.getHistory()["time"], y=np.array(valve.getHistory()["massFlowRate"]) * 1000,
                              mode='lines',
                              name='mass flow rate',
                              line_color=px.colors.qualitative.Plotly[3],
                              showlegend=True),
                   row=2, col=2)

    # Update xaxis properties
    fig2.update_xaxes(title_text="Time [s]", range=[0, 0.1])

    # Update yaxis properties
    fig2.update_yaxes(title_text="Pressure [bar]", row=1, col=1)
    fig2.update_yaxes(title_text="Temperature [K]", row=1, col=2)
    fig2.update_yaxes(title_text="Density [kg/m^3]", row=2, col=1)
    fig2.update_yaxes(title_text="Mass [g]", row=2, col=2)

    fig.show()
    fig2.show()