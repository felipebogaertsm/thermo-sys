"""
Miscellaneous functions.
"""

from pyfluids import Fluid


def print_states(states: list[Fluid]) -> None:
    for i, state in enumerate(states):
        print(
            f"{i+1} - {state.name}: {state.pressure * 1e-5:.2f} bar,"
            f" {state.temperature:.2f} C, {state.enthalpy * 1e-3:.2f} kJ/kg"
        )
