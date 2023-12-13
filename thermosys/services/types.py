"""
Types.
"""

from typing import Union
from pyfluids import Fluid

# Define a custom type for device details in the thermodynamic cycle
DeviceDetails = dict[str, dict[str, list[int]]]

"""
Type for a thermodynamic cycle output.

Example:
{
    "efficiency": 0.85,
    "bwr": 0.1,
    "states": [Fluid(...), Fluid(...)],
    "devices": {
        "Turbine": {"inlets": [0], "outlets": [1]},
        "Compressor": {"inlets": [2], "outlets": [3, 4]}
    }
}
"""
ThermodynamicCycleOutput = dict[str, Union[float, list[Fluid], DeviceDetails]]
