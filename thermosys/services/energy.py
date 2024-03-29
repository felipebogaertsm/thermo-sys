"""
Energy calculation functions.
"""

import numpy as np
from pyfluids import Fluid


def energy_balance(state_1: Fluid, state_2: Fluid) -> float:
    """
    Calculates the energy balance between two states.
    """
    return np.abs(state_2.enthalpy - state_1.enthalpy)
