"""
Gas specific devices.
"""

from pyfluids import Fluid, Input


def compress_to(
    inlet_state: Fluid,
    efficiency: float,
    compression_ratio: float,
) -> Fluid:
    """
    Compresses a fluid to a specified state based on the given efficiency and
    compression ratio.

    Parameters:
    inlet_state (Fluid): The state of the fluid at the inlet of the compressor.
    efficiency (float): The efficiency of the compressor (as a decimal).
    compression_ratio (float): The ratio of the outlet pressure to the inlet
        pressure.

    Returns:
    Fluid: The state of the fluid at the outlet of the compressor.
    """
    inlet_pressure = inlet_state.pressure
    inlet_temperature = inlet_state.temperature

    outlet_pressure = inlet_pressure * compression_ratio

    fluid = inlet_state.with_state(
        Input.pressure(inlet_pressure),
        Input.temperature(inlet_temperature),
    )

    outlet_state = fluid.compression_to_pressure(
        pressure=outlet_pressure,
        isentropic_efficiency=efficiency * 100,
    )

    return outlet_state
