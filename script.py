"""
Script file used for testing classes and functions.
"""

from pyfluids import Fluid, FluidsList, Input

from thermosys.models.cycles import BraytonCycle
from thermosys.models.devices import (
    HeatSourceDevice,
    GasCompressor,
    Turbine,
    Condenser,
    Pump,
    Deaerator,
)
from thermosys.services.units import bar_to_pascal, pascal_to_bar

BRAYTON_INLET_PRESSURE = bar_to_pascal(1)  # Pa
BRAYTON_INLET_TEMPERATURE = 30  # C
BRAYTON_MASS_FLUX = 450  # kg/s
BRAYTON_COMPRESSOR_EFFICIENCY = 0.8  # -
BRAYTON_COMPRESSION_RATIO = 25  # -
BRAYTON_TURBINE_C_EFFICIENCY = 0.8  # -
BRAYTON_COMBUSTION_CHAMBER_1_TEMPERATURE = 1000  # C
BRAYTON_TURBINE_P_EFFICIENCY = 0.85  # -
BRAYTON_COMBUSTION_CHAMBER_2_TEMPERATURE = 710  # C
RECOVERY_BOILER_DELTA_TSA = 25  # C
RANKINE_DESAERATOR_PRESSURE = bar_to_pascal(5)  # Pa
RANKINE_TURBINE_EFFICIENCY = 0.9  # -
RANKINE_CONDENSER_PRESSURE = bar_to_pascal(0.1)  # Pa
RANKINE_PUMP_EFFICIENCY = 0.9999  # -
RANKINE_DEAERATOR_TEMPERATURE = 120  # C

# Optimization variable:
vapor_inlet_pressure = bar_to_pascal(10)  # Pa


gas_initial_state = Fluid(FluidsList.Air).with_state(
    Input.pressure(BRAYTON_INLET_PRESSURE),
    Input.temperature(BRAYTON_INLET_TEMPERATURE),
)

# BRAYTON CYCLE:
brayton_cycle = BraytonCycle(
    initial_state=gas_initial_state, mass_flux=BRAYTON_MASS_FLUX
)

# Defining devices:
compressor_1g = GasCompressor(
    name="C1g",
    efficiency=BRAYTON_COMPRESSOR_EFFICIENCY,
    compression_ratio=BRAYTON_COMPRESSION_RATIO,
)
combustion_chamber_1g = HeatSourceDevice(
    name="CC1g",
    fluid_type=FluidsList.Air,
    outlet_temperature=BRAYTON_COMBUSTION_CHAMBER_1_TEMPERATURE,
)

state_1g = brayton_cycle.initial_state
state_2g = compressor_1g.get_outlet_state(state_1g)
state_3g = combustion_chamber_1g.get_outlet_state(state_2g)

turbine_1g = Turbine(
    name="TCg",
    efficiency=BRAYTON_TURBINE_C_EFFICIENCY,
    fluid_type=FluidsList.Air,
    outlet_pressure=bar_to_pascal(10),
    energy_balance=state_2g.enthalpy - state_1g.enthalpy,
)
combustion_chamber_2g = HeatSourceDevice(
    name="CC2g",
    fluid_type=FluidsList.Air,
    outlet_temperature=BRAYTON_COMBUSTION_CHAMBER_2_TEMPERATURE,
)
turbine_2g = Turbine(
    name="TPg",
    efficiency=BRAYTON_TURBINE_P_EFFICIENCY,
    fluid_type=FluidsList.Air,
    outlet_pressure=BRAYTON_INLET_PRESSURE,
)

state_4g = turbine_1g.get_outlet_state(state_3g)
state_5g = combustion_chamber_2g.get_outlet_state(state_4g)
state_6g = turbine_2g.get_outlet_state(state_5g)

devices = [
    compressor_1g,
    combustion_chamber_1g,
    turbine_1g,
    combustion_chamber_2g,
    turbine_2g,
]

states = [state_1g, state_2g, state_3g, state_4g, state_5g, state_6g]

brayton_cycle.devices = devices
brayton_cycle.states = states

brayton_cycle.print_results()

# RANKINE CYCLE:
vapor_initial_temperature = state_6g.temperature - RECOVERY_BOILER_DELTA_TSA
vapor_initial_state = Fluid(FluidsList.Water).with_state(
    Input.pressure(vapor_inlet_pressure),
    Input.temperature(vapor_initial_temperature),
)

recovery_boiler = HeatSourceDevice(
    name="RB",
    fluid_type=FluidsList.Water,
    outlet_temperature=vapor_initial_temperature,
)

state_1v = recovery_boiler.get_outlet_state(vapor_initial_state)

vapor_turbine_1 = Turbine(
    name="T1v",
    efficiency=RANKINE_TURBINE_EFFICIENCY,
    fluid_type=FluidsList.Water,
    outlet_pressure=RANKINE_DESAERATOR_PRESSURE,
)

state_2v = vapor_turbine_1.get_outlet_state(state_1v)

vapor_turbine_2 = Turbine(
    name="T2v",
    efficiency=RANKINE_TURBINE_EFFICIENCY,
    fluid_type=FluidsList.Water,
    outlet_pressure=RANKINE_CONDENSER_PRESSURE,
)

state_3v = vapor_turbine_2.get_outlet_state(state_2v)

vapor_condenser = Condenser(
    name="Cv",
    fluid_type=FluidsList.Water,
    pressure=RANKINE_CONDENSER_PRESSURE,
)

state_4v = vapor_condenser.get_outlet_state(state_3v)

vapor_pump_1 = Pump(
    name="Pv",
    efficiency=RANKINE_PUMP_EFFICIENCY,
    outlet_pressure=RANKINE_DESAERATOR_PRESSURE,
)

state_5v = vapor_pump_1.get_outlet_state(state_4v)

vapor_deaerator = Deaerator(
    name="Dv",
    temperature=RANKINE_DESAERATOR_PRESSURE,
)

state_7v = Fluid(FluidsList.Water).with_state(
    Input.pressure(RANKINE_DESAERATOR_PRESSURE),
    Input.temperature(RANKINE_DEAERATOR_TEMPERATURE),
)

vapor_pump_2 = Pump(
    name="Pv",
    efficiency=RANKINE_PUMP_EFFICIENCY,
    outlet_pressure=vapor_inlet_pressure,
)

state_6v = vapor_pump_2.get_inlet_state(state_7v)
