"""
Defines classes that represent devices in a thermodynamic cycle.
These classes are generally behavioral, so regular classes instead of 
dataclasses will be used.
"""

from abc import ABC, abstractmethod

from thermosys.models.generic import State


class Device(ABC):
    """
    Represents a general device in a thermodynamic cycle.

    Attributes:
    name (str): The name or identifier of the device.
    efficiency (float): The efficiency of the device (as a decimal).

    Methods:
    __init__: Initializes a new instance of the Device class.
    get_outlet_state: Returns the state of the gas at the outlet of the device.
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

    @abstractmethod
    def get_outlet_state(self, *args, **kwargs) -> State:
        """
        Returns the state of the gas at the outlet of the device.

        Returns:
        State: The state of the gas at the outlet of the device.
        """


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


class CombustionChamber(Device):
    """
    Represents a combustion chamber in a thermodynamic cycle.

    Attributes:
    outlet_temperature (float): The temperature of the gas at the outlet of
        the combustion chamber (C).

    Methods:
    __init__: Initializes a new instance of the CombustionChamber class.
    """

    def __init__(
        self, name: str, efficiency: float, outlet_temperature: float
    ) -> None:
        """
        Initializes a new instance of the CombustionChamber class.

        Parameters:
        name (str): The name or identifier of the combustion chamber.
        efficiency (float): The efficiency of the combustion process (as a
            decimal).
        outlet_temperature (float): The temperature of the gas at the outlet
            of the combustion chamber (in Kelvin).
        """
        super().__init__(name, efficiency)
        self.outlet_temperature = outlet_temperature


class GasTurbine(Device):
    """
    Represents a gas turbine in a thermodynamic cycle.

    Attributes:
    inlet_pressure (float): The pressure of the gas at the inlet of the turbine (in Pascals).
    outlet_pressure (float): The pressure of the gas at the outlet of the turbine (in Pascals).

    Methods:
    __init__: Initializes a new instance of the GasTurbine class.
    """

    def __init__(
        self,
        name: str,
        efficiency: float,
        inlet_pressure: float,
        outlet_pressure: float,
    ) -> None:
        """
        Initializes a new instance of the GasTurbine class.

        Parameters:
        name (str): The name or identifier of the gas turbine.
        efficiency (float): The efficiency of the turbine (as a decimal).
        inlet_pressure (float): The pressure of the gas at the inlet of the turbine (in Pascals).
        outlet_pressure (float): The pressure of the gas at the outlet of the turbine (in Pascals).
        """
        super().__init__(name, efficiency)
        self.inlet_pressure = inlet_pressure
        self.outlet_pressure = outlet_pressure
