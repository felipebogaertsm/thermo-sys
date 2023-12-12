"""
Exemplo de uso do thermo-sys.
"""

from pyfluids import Fluid, FluidsList, Input

from thermosys.models.cycles import BraytonCycle
from thermosys.models.devices import (
    GasCombustionChamber,
    GasCompressor,
    GasTurbine,
)
from thermosys.services.units import bar_to_pascal

gas_initial_state = Fluid(FluidsList.Air).with_state(
    Input.pressure(bar_to_pascal(1)),
    Input.temperature(30),
)

# Creating Brayton cycle instance:
brayton_cycle = BraytonCycle(initial_state=gas_initial_state, mass_flux=450)

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
    outlet_pressure=bar_to_pascal(8),
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

# Results:
print("BRAYTON GAS CYCLE\n")

for i, state in enumerate(states):
    print(
        f"{i+1} - {state.name}: {state.pressure * 1e-5:.2f} bar, {state.temperature:.2f} C, {state.enthalpy * 1e-3:.2f} kJ/kg"
    )

print("\n")

for device in devices:
    print(
        f"{device.name}: {device.energy_balance * 1e-3:.2f} kJ/kg",
    )

print("\n")

print(f"Turbine work: {brayton_cycle.turbine_work * 1e-3:.2f} kJ/kg")
print(f"Compressor work: {brayton_cycle.compressor_work * 1e-3:.2f} kJ/kg")
print(
    f"Total work: {(brayton_cycle.turbine_work - brayton_cycle.compressor_work) * 1e-3:.2f} kJ/kg"
)
print(f"Heat input: {brayton_cycle.heat_in * 1e-3:.2f} kJ/kg")

print("\n")

print(f"Efficiency: {brayton_cycle.get_efficiency() * 100:.2f} %")
