from pyfluids import Fluid, FluidsList, Input

from thermosys.services.units import bar_to_pascal

AMBIENT_PRESSURE = bar_to_pascal(1)  # Pa
AMBIENT_TEMPERATURE = 30  # C

DELTA_TP = 10  # C
DELTA_TE = 10  # C


def recovery_boiler_example(
    inlet_boiler_pressure: float,
    inlet_gas_pressure: float,
) -> float:
    state_8_evaporator = Fluid(FluidsList.Water).two_phase_point_at_pressure(
        pressure=inlet_boiler_pressure,
        quality=0,
    )

    state_12 = Fluid(FluidsList.Water).two_phase_point_at_pressure(
        pressure=inlet_boiler_pressure,
        quality=1,
    )

    temperature_a = state_8_evaporator.temperature + DELTA_TP
    state_a = Fluid(FluidsList.Air).with_state(
        Input.pressure(inlet_gas_pressure),
        Input.temperature(temperature_a),
    )

    temperature_8_economizer = state_8_evaporator.temperature - DELTA_TE
    state_8_economizer = Fluid(FluidsList.Water).with_state(
        Input.pressure(inlet_boiler_pressure),
        Input.temperature(temperature_8_economizer),
    )

    state_ambient = Fluid(FluidsList.Air).with_state(
        Input.pressure(AMBIENT_PRESSURE),
        Input.temperature(AMBIENT_TEMPERATURE),
    )

    enthalpy_7_gas = state_a.enthalpy

    return ()
