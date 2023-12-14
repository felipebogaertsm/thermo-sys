"""
Vapor specific devices.
"""

from pyfluids import Fluid, FluidsList, Input


def condense_to_pressure(inlet_state: Fluid) -> Fluid:
    """
    Determines the outlet state of a condenser based on a given outlet
        pressure.

    Parameters:
    inlet_state (Fluid): The inlet state of the fluid.

    Returns:
    Fluid: The outlet state of the fluid after condensation.
    """
    saturation_state = inlet_state.two_phase_point_at_pressure(
        pressure=inlet_state.pressure,
        quality=0,
    )

    return saturation_state


def pump_to_pressure(
    inlet_state: Fluid, efficiency: float, outlet_pressure: float
) -> Fluid:
    """
    Determines the outlet state of a pump based on the given efficiency and
    outlet pressure.

    Parameters:
    inlet_state (Fluid): The inlet state of the fluid.
    efficiency (float): The efficiency of the pump (as a decimal).
    outlet_pressure (float): The desired outlet pressure of the fluid in the
        pump (in Pascals).

    Returns:
    Fluid: The outlet state of the fluid after compression in the pump.
    """
    outlet_state = inlet_state.compression_to_pressure(
        pressure=outlet_pressure,
        isentropic_efficiency=efficiency * 100,
    )

    return outlet_state
