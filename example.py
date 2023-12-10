"""
Exemplo de uso do thermo-sys.
"""

from thermosys.models.cycles import BraytonCycle
from thermosys.models.devices import (
    CombustionChamber,
    GasCompressor,
    GasTurbine,
)

# Creating 1st Brayton cycle instance:
brayton_cycle_1 = BraytonCycle(
    ambient_temperature=25, ambient_pressure=101325, mass_flux=450
)
brayton_cycle_1.add_device(
    GasCompressor(
        name="C1g1",
        inlet_pressure=101325,
        compression_ratio=10,
        efficiency=0.8,
    )
)
brayton_cycle_1.add_device(
    CombustionChamber(
        name="CC1g1",
        efficiency=1,
        outlet_temperature=1000,
    )
)
brayton_cycle_1.add_device(
    GasTurbine(
        name="TCg1",
        efficiency=0.8,
        inlet_pressure=101325,
        outlet_pressure=101325,
    )
)
brayton_cycle_1.add_device(
    CombustionChamber(
        name="CC1g1",
        efficiency=1,
        outlet_temperature=710,
    )
)
brayton_cycle_1.add_device(
    GasTurbine(
        name="TPg1",
        efficiency=0.85,
        inlet_pressure=101325,
        outlet_pressure=101325,
    )
)

# Creating 2nd Brayton cycle instance:
brayton_cycle_2 = BraytonCycle(
    ambient_temperature=25, ambient_pressure=101325, mass_flux=450
)
brayton_cycle_2.add_device(
    GasCompressor(
        name="C1g2",
        inlet_pressure=101325,
        compression_ratio=10,
        efficiency=0.8,
    )
)
brayton_cycle_2.add_device(
    CombustionChamber(
        name="CC1g2",
        efficiency=1,
        outlet_temperature=1000,
    )
)
brayton_cycle_2.add_device(
    GasTurbine(
        name="TCg2",
        efficiency=0.8,
        inlet_pressure=101325,
        outlet_pressure=101325,
    )
)
brayton_cycle_2.add_device(
    CombustionChamber(
        name="CC1g2",
        efficiency=1,
        outlet_temperature=710,
    )
)
brayton_cycle_2.add_device(
    GasTurbine(
        name="TPg2",
        efficiency=0.85,
        inlet_pressure=101325,
        outlet_pressure=101325,
    )
)
