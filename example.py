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
        outlet_pressure=101325 * 3,
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
