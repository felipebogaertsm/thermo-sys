"""
Cogeneration example from the examples in gas.py and vapor.py.
"""

from gas import brayton_cycle_example
from vapor import rankine_cycle_example
from thermosys.services.misc import print_states
from thermosys.services.units import bar_to_pascal

# Optimization variable:
vapor_inlet_pressure = bar_to_pascal(10)  # Pa


def main():
    # Solve brayton cycle:
    brayton_cycle = brayton_cycle_example()
    gas_states = brayton_cycle["states"]
    print("BRAYTON CYCLE")
    print_states(gas_states)

    print("\n")

    # Solve rankine cycle:
    rankine_cycle = rankine_cycle_example(
        gas_outlet_state=gas_states[-1],
        inlet_pressure=vapor_inlet_pressure,
    )
    print("RANKINE CYCLE")
    print_states(rankine_cycle["states"])


if __name__ == "__main__":
    main()
