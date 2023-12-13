"""
Vapor specific devices.
"""

from pyfluids import Fluid


def condense_to_pressure(inlet_state: Fluid, outlet_pressure: float) -> Fluid:
    """
    Determines the outlet state of a condenser based on a given outlet
        pressure.

    Parameters:
    inlet_state (Fluid): The inlet state of the fluid.
    outlet_pressure (float): The desired outlet pressure of the fluid in the
        condenser (in Pascals).

    Returns:
    Fluid: The outlet state of the fluid after condensation.
    """
    # Determine the saturated fluid state at the given outlet pressure
    saturated_fluid = inlet_state.dew_point_at_pressure(
        pressure=outlet_pressure
    )

    return saturated_fluid


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
