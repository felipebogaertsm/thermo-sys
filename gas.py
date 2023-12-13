"""
Brayton cycle example.
"""

from pyfluids import Fluid, FluidsList, Input

from thermosys.processes import (
    heat_to_temperature,
    turbine_to_enthalpy,
    turbine_to_pressure,
)
from thermosys.processes.gas import compress_to
from thermosys.services.energy import energy_balance
from thermosys.services.types import ThermodynamicCycleOutput
from thermosys.services.units import bar_to_pascal

INLET_PRESSURE = bar_to_pascal(1)  # Pa
INLET_TEMPERATURE = 30  # C
MASS_FLUX = 450  # kg/s
COMPRESSOR_EFFICIENCY = 0.8  # -
COMPRESSION_RATIO = 25  # -
TURBINE_C_EFFICIENCY = 0.8  # -
COMBUSTION_CHAMBER_1_TEMPERATURE = 1000  # C
TURBINE_P_EFFICIENCY = 0.85  # -
COMBUSTION_CHAMBER_2_TEMPERATURE = 710  # C


def brayton_cycle_example() -> ThermodynamicCycleOutput:
    """
    Brayton cycle example.

    Returns:
    ThermodynamicCycleOutput: Thermodynamic cycle output.
    """
    state_1 = Fluid(FluidsList.Air).with_state(
        Input.pressure(INLET_PRESSURE),
        Input.temperature(INLET_TEMPERATURE),
    )

    state_2 = compress_to(
        inlet_state=state_1,
        efficiency=COMPRESSOR_EFFICIENCY,
        compression_ratio=COMPRESSION_RATIO,
    )

    state_3 = heat_to_temperature(
        inlet_state=state_2,
        outlet_temperature=COMBUSTION_CHAMBER_1_TEMPERATURE,
    )

    energy_balance_compressor = energy_balance(state_1, state_2)
    state_4 = turbine_to_enthalpy(
        inlet_state=state_3,
        efficiency=TURBINE_C_EFFICIENCY,
        energy_balance=energy_balance_compressor,
    )

    state_5 = heat_to_temperature(
        inlet_state=state_4,
        outlet_temperature=COMBUSTION_CHAMBER_2_TEMPERATURE,
    )

    state_6 = turbine_to_pressure(
        inlet_state=state_5,
        efficiency=TURBINE_P_EFFICIENCY,
        outlet_pressure=INLET_PRESSURE,
    )

    return {
        "states": [state_1, state_2, state_3, state_4, state_5, state_6],
    }
