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
brayton_cycle.add_device(
    GasCompressor(
        name="C1g",
        efficiency=0.8,
        compression_ratio=25,
    )
)
brayton_cycle.add_device(
    GasCombustionChamber(
        name="CC1g",
        outlet_temperature=1000,
    )
)
brayton_cycle.add_device(
    GasTurbine(
        name="TCg",
        efficiency=0.8,
        outlet_pressure=bar_to_pascal(5),
    )
)
brayton_cycle.add_device(
    GasCombustionChamber(
        name="CC2g",
        outlet_temperature=710,
    )
)
brayton_cycle.add_device(
    GasTurbine(
        name="TPg",
        efficiency=0.85,
        outlet_pressure=101325,
    )
)

brayton_cycle.solve()

# Results:
print("BRAYTON GAS CYCLE\n")

for i, state in enumerate(brayton_cycle.states):
    print(
        f"{i+1} - {state.name}: {state.pressure * 1e-5:.2f} bar, {state.temperature:.2f} C, {state.enthalpy * 1e-3:.2f} kJ/kg"
    )

print("\n")

for device in brayton_cycle.devices:
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
