"""
Defines classes that represent devices in a thermodynamic cycle.
These classes are generally behavioral, so regular classes instead of 
dataclasses will be used.
"""


class Device:
    """
    Represents a general device in a thermodynamic cycle.

    Attributes:
    name (str): The name or identifier of the device.
    efficiency (float): The efficiency of the device (as a decimal).

    Methods:
    __init__: Initializes a new instance of the Device class.
    """

    def __init__(self, name: str, efficiency: float) -> None:
        """
        Initializes a new instance of the Device class.

        Parameters:
        name (str): The name or identifier of the device.
        efficiency (float): The efficiency of the device (as a decimal).
        """
        self.name = name
        self.efficiency = efficiency


class GasCompressor(Device):
    """
    Represents a gas compressor in a thermodynamic cycle, inheriting from the Device class.

    Attributes:
    inlet_pressure (float): The inlet pressure of the gas before compression (in Pascals).
    compression_ratio (float): The ratio of the outlet pressure to the inlet pressure.

    Methods:
    __init__: Initializes a new instance of the GasCompressor class.
    """

    def __init__(
        self,
        name: str,
        efficiency: float,
        inlet_pressure: float,
        compression_ratio: float,
    ) -> None:
        """
        Initializes a new instance of the GasCompressor class.

        Parameters:
        name (str): The name or identifier of the compressor.
        efficiency (float): The efficiency of the compressor (as a decimal).
        inlet_pressure (float): The inlet pressure of the gas before compression (in Pascals).
        compression_ratio (float): The ratio of the outlet pressure to the inlet pressure.
        """
        super().__init__(name, efficiency)
        self.inlet_pressure = inlet_pressure
        self.compression_ratio = compression_ratio
