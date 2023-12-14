"""
Cogeneration example from the examples in gas.py and vapor.py.
"""

import numpy as np

from example_gas import brayton_cycle_example
from example_vapor import rankine_cycle_example
from thermosys.services.energy import energy_balance
from thermosys.services.misc import print_states
from thermosys.services.montecarlo import get_random_value, plot_monte_carlo
from thermosys.services.units import bar_to_pascal

ITERATION_COUNT = 1000  # -


def main():
    # Solve brayton cycle:
    brayton_cycle = brayton_cycle_example()
    gas_states = brayton_cycle["states"]
    print("BRAYTON CYCLE")
    print_states(gas_states)

    gas_turbine_specific_work = energy_balance(
        gas_states[3], gas_states[2]
    ) + energy_balance(gas_states[5], gas_states[4])
    gas_compressor_specific_work = energy_balance(gas_states[0], gas_states[1])
    gas_net_specific_work = (
        gas_turbine_specific_work - gas_compressor_specific_work
    )
    gas_specific_heat_in = energy_balance(
        gas_states[1], gas_states[2]
    ) + energy_balance(gas_states[3], gas_states[4])

    gas_efficiency = gas_net_specific_work / gas_specific_heat_in
    gas_bwr = gas_turbine_specific_work / gas_compressor_specific_work

    print("\n")

    print(
        f"Gas turbine specific work: {gas_turbine_specific_work * 1e-3:.2f} kJ/kg"
    )
    print(
        f"Gas compressor specific work: {gas_compressor_specific_work * 1e-3:.2f} kJ/kg"
    )
    print(f"Gas net specific work: {gas_net_specific_work * 1e-3:.2f} kJ/kg")
    print(f"Gas specific heat in: {gas_specific_heat_in * 1e-3:.2f} kJ/kg")
    print(f"Gas thermal efficiency: {gas_efficiency * 100:.2f} %")
    print(f"Gas BWR: {gas_bwr * 100:.2f} %")

    print("\n")

    # Solve rankine cycle:
    rankine_cycle = rankine_cycle_example(
        gas_outlet_state=gas_states[-1],
        inlet_pressure=bar_to_pascal(10),
    )
    print("RANKINE CYCLE")
    print_states(rankine_cycle["states"])

    pressure = np.array([])
    efficiency = np.array([])

    for _ in range(ITERATION_COUNT):
        vapor_inlet_pressure = get_random_value(
            5, 200
        )  # deaerator pressure minimum

        # Solve Rankine cycle:
        rankine_cycle = rankine_cycle_example(
            gas_outlet_state=gas_states[-1],
            inlet_pressure=bar_to_pascal(vapor_inlet_pressure),
        )

        vapor_states = rankine_cycle["states"]

        vapor_turbine_specific_work = energy_balance(
            vapor_states[1], vapor_states[0]
        ) + energy_balance(vapor_states[2], vapor_states[1])
        vapor_pump_specific_work = energy_balance(
            vapor_states[3], vapor_states[4]
        ) + energy_balance(vapor_states[5], vapor_states[6])
        vapor_net_specific_work = (
            vapor_turbine_specific_work - vapor_pump_specific_work
        )
        vapor_specific_heat_in = energy_balance(
            vapor_states[-1], vapor_states[0]
        )

        vapor_efficiency = vapor_net_specific_work / vapor_specific_heat_in

        pressure = np.append(pressure, vapor_inlet_pressure)
        efficiency = np.append(efficiency, vapor_efficiency)
        print_states(vapor_states)

    max_efficiency = np.max(efficiency)
    pressure_at_max_efficiency = pressure[efficiency == max_efficiency]

    print("\n")

    print(f"Max efficiency: {max_efficiency * 100:.2f} %")
    print(
        f"Vapor inlet pressure for max efficiency: {pressure_at_max_efficiency[0]:.2f} bar"
    )

    plot_monte_carlo(pressure, efficiency)


if __name__ == "__main__":
    main()
