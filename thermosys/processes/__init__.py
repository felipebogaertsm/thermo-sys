"""
Devices that are fluid agnostic.
"""

import numpy as np
from pyfluids import Fluid, Input


def heat_to_temperature(
    inlet_state: Fluid, outlet_temperature: float
) -> Fluid:
    """
    Heats a fluid to a specified outlet temperature.

    Parameters:
    inlet_state (Fluid): The state of the fluid at the inlet of the heat
        source.
    outlet_temperature (float): The target temperature of the fluid at the outlet of the heat source (in °C).

    Returns:
    Fluid: The state of the fluid at the outlet after heating.
    """
    # Use the specified fluid type for setting the state
    fluid = inlet_state.with_state(
        Input.pressure(inlet_state.pressure),
        Input.temperature(outlet_temperature),
    )

    return fluid


def turbine_to_pressure(
    inlet_state: Fluid,
    efficiency: float,
    outlet_pressure: float,
) -> Fluid:
    """
    Determines the outlet state of a turbine based on a given outlet pressure.

    Parameters:
    inlet_state (Fluid): The inlet state of the fluid.
    efficiency (float): The efficiency of the turbine (as a decimal).
    outlet_pressure (float): The desired outlet pressure (in Pascals).

    Returns:
    Fluid: The outlet state of the fluid after expansion to the given outlet pressure.
    """
    outlet_state = inlet_state.expansion_to_pressure(
        pressure=outlet_pressure,
        isentropic_efficiency=efficiency * 100,
    )
    return outlet_state


def turbine_to_enthalpy(
    inlet_state: Fluid,
    efficiency: float,
    energy_balance: float,
) -> Fluid:
    """
    Determines the outlet state of a turbine based on the specified energy balance.

    Parameters:
    inlet_state (Fluid): The inlet state of the fluid.
    efficiency (float): The efficiency of the turbine (as a decimal).
    energy_balance (float): The energy balance to be achieved (in J/kg).

    Returns:
    Fluid: The outlet state of the fluid after cooling to achieve the given energy balance.
    """
    outlet_enthalpy = inlet_state.enthalpy - energy_balance / efficiency
    pressure_drop = np.abs(
        inlet_state.pressure
        - inlet_state.pressure * (outlet_enthalpy / inlet_state.enthalpy)
    )

    outlet_state = inlet_state.cooling_to_enthalpy(
        enthalpy=outlet_enthalpy, pressure_drop=pressure_drop
    )
    return outlet_state
