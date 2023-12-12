"""
Exemplo de uso do thermo-sys.
"""

from plotly import graph_objects as go
from pyfluids import Fluid, FluidsList, Input

from thermosys.models.cycles import BraytonCycle
from thermosys.models.devices import (
    GasCombustionChamber,
    GasCompressor,
    GasTurbine,
)
from thermosys.services.montecarlo import get_random_value
from thermosys.services.units import bar_to_pascal, pascal_to_bar


def simulate_system(brayton_tc_outlet_pressure: float) -> float:
    gas_initial_state = Fluid(FluidsList.Air).with_state(
        Input.pressure(bar_to_pascal(1)),
        Input.temperature(30),
    )

    # Creating Brayton cycle instance:
    brayton_cycle = BraytonCycle(
        initial_state=gas_initial_state, mass_flux=450
    )

    # Defining devices:
    compressor_1g = GasCompressor(
        name="C1g",
        efficiency=0.8,
        compression_ratio=25,
    )
    combustion_chamber_1g = GasCombustionChamber(
        name="CC1g",
        outlet_temperature=1000,
    )

    state_1g = brayton_cycle.initial_state
    state_2g = compressor_1g.get_outlet_state(state_1g)
    state_3g = combustion_chamber_1g.get_outlet_state(state_2g)

    turbine_1g = GasTurbine(
        name="TCg",
        efficiency=0.8,
        outlet_pressure=brayton_tc_outlet_pressure,
        energy_balance=state_2g.enthalpy - state_1g.enthalpy,
    )
    combustion_chamber_2g = GasCombustionChamber(
        name="CC2g",
        outlet_temperature=710,
    )
    turbine_2g = GasTurbine(
        name="TPg",
        efficiency=0.85,
        outlet_pressure=bar_to_pascal(1),
    )

    state_4g = turbine_1g.get_outlet_state(state_3g)
    state_5g = combustion_chamber_2g.get_outlet_state(state_4g)
    state_6g = turbine_2g.get_outlet_state(state_5g)

    devices = [
        compressor_1g,
        combustion_chamber_1g,
        turbine_1g,
        combustion_chamber_2g,
        turbine_2g,
    ]

    states = [state_1g, state_2g, state_3g, state_4g, state_5g, state_6g]

    brayton_cycle.devices = devices
    brayton_cycle.states = states

    return brayton_cycle.get_efficiency()


def montecarlo_optimization() -> tuple[float]:
    """
    This function runs a montecarlo optimization for the thermodynamic
    system.
    """
    iterations = 1000
    results = []

    for i in range(iterations):
        # Generating random values for the pressure drop in the turbine:
        brayton_tc_outlet_pressure = get_random_value(
            min_value=bar_to_pascal(1.01),
            max_value=bar_to_pascal(24.99),
        )

        # Simulating the system:
        efficiency = simulate_system(brayton_tc_outlet_pressure)

        # Saving the results:
        results.append((efficiency, brayton_tc_outlet_pressure))

    return results


results = montecarlo_optimization()

# Extracting efficiency and pressure for plotting
efficiencies, pressures = zip(*results)

pressures_in_bar = [pascal_to_bar(p) for p in pressures]
efficiencies_in_percent = [e * 100 for e in efficiencies]

# Creating the plot
fig = go.Figure(
    data=[
        go.Scatter(
            x=pressures_in_bar,
            y=efficiencies_in_percent,
            mode="markers",
        )
    ]
)
fig.update_layout(
    title="Monte Carlo Optimization of Thermodynamic System",
    xaxis_title="Pressure (bar)",
    yaxis_title="Efficiency",
)

# Display the plot
fig.show()
