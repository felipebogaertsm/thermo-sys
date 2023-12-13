"""
Rankine cycle example.
"""

from pyfluids import Fluid, FluidsList, Input

from thermosys.processes import (
    heat_to_temperature,
    turbine_to_pressure,
)
from thermosys.processes.vapor import condense_to_pressure, pump_to_pressure
from thermosys.services.types import ThermodynamicCycleOutput
from thermosys.services.units import bar_to_pascal

RECOVERY_BOILER_DELTA_TSA = 25  # C

DEAERATOR_PRESSURE = bar_to_pascal(5)  # Pa
TURBINE_EFFICIENCY = 0.9  # -
CONDENSER_PRESSURE = bar_to_pascal(0.1)  # Pa
PUMP_EFFICIENCY = 0.9999  # -
DEAERATOR_TEMPERATURE = 120  # C


def rankine_cycle_example(
    gas_outlet_state: float,
    inlet_pressure: float,
) -> ThermodynamicCycleOutput:
    """
    Rankine cycle example.

    Args:
    gas_outlet_state (Fluid): Gas outlet state.
    inlet_pressure (float): Inlet pressure.

    Returns:
    ThermodynamicCycleOutput: Thermodynamic cycle output.
    """
    state_7 = Fluid(FluidsList.Water).with_state(
        Input.pressure(inlet_pressure),
        Input.temperature(DEAERATOR_TEMPERATURE),
    )

    state_1 = heat_to_temperature(
        inlet_state=state_7,
        outlet_temperature=gas_outlet_state.temperature
        - RECOVERY_BOILER_DELTA_TSA,
    )

    state_2 = turbine_to_pressure(
        inlet_state=state_1,
        efficiency=TURBINE_EFFICIENCY,
        outlet_pressure=DEAERATOR_PRESSURE,
    )

    state_3 = turbine_to_pressure(
        inlet_state=state_2,
        efficiency=TURBINE_EFFICIENCY,
        outlet_pressure=CONDENSER_PRESSURE,
    )

    state_4 = condense_to_pressure(
        inlet_state=state_3,
    )

    state_5 = pump_to_pressure(
        inlet_state=state_4,
        efficiency=PUMP_EFFICIENCY,
        outlet_pressure=DEAERATOR_PRESSURE,
    )

    state_6 = state_5.with_state(
        Input.pressure(state_5.pressure),
        Input.entropy(state_7.entropy),
    )

    return {
        "states": [
            state_1,
            state_2,
            state_3,
            state_4,
            state_5,
            state_6,
            state_7,
        ],
    }
