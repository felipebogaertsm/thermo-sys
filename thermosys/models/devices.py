"""
Defines classes that represent devices in a thermodynamic cycle.
These classes are generally behavioral, so regular classes instead of 
dataclasses will be used.
"""

from abc import ABC, abstractmethod

from pyfluids import Fluid, FluidsList, Input


class Device(ABC):
    """
    Represents a general device in a thermodynamic cycle.

    Attributes:
    name (str): The name or identifier of the device.

    Methods:
    __init__: Initializes a new instance of the Device class.
    get_outlet_state: Returns the state of the gas at the outlet of the device.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the Device class.

        Parameters:
        name (str): The name or identifier of the device.
        """
        self.name = name

    @abstractmethod
    def get_outlet_state(self, inlet_state: Fluid, *args, **kwargs) -> Fluid:
        """
        Returns the state of the gas at the outlet of the device.

        Parameters:
        inlet_state (Fluid): The state of the gas at the inlet of the device.

        Returns:
        Fluid: The state of the gas at the outlet of the device.
        """


class NonIsentropicDevice(Device):
    """
    Represents a general non-isentropic device in a thermodynamic cycle.

    Attributes:
    efficiency (float): The efficiency of the device (as a decimal).

    Methods:
    __init__: Initializes a new instance of the NonIsentropicDevice class.
    """

    def __init__(self, name: str, efficiency: float) -> None:
        """
        Initializes a new instance of the NonIsentropicDevice class.

        Parameters:
        name (str): The name or identifier of the device.
        efficiency (float): The efficiency of the device (as a decimal).
        """
        super().__init__(name)
        self.efficiency = efficiency


class GasCompressor(NonIsentropicDevice):
    """
    Represents a gas compressor in a thermodynamic cycle, inheriting from the Device class.

    Attributes:
    compression_ratio (float): The ratio of the outlet pressure to the inlet pressure.

    Methods:
    __init__: Initializes a new instance of the GasCompressor class.
    """

    def __init__(
        self,
        name: str,
        efficiency: float,
        compression_ratio: float,
    ) -> None:
        """
        Initializes a new instance of the GasCompressor class.

        Parameters:
        name (str): The name or identifier of the compressor.
        efficiency (float): The efficiency of the compressor (as a decimal).
        compression_ratio (float): The ratio of the outlet pressure to the inlet pressure.
        """
        super().__init__(name, efficiency)
        self.compression_ratio = compression_ratio

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        inlet_pressure = inlet_state.pressure
        inlet_temperature = inlet_state.temperature

        outlet_pressure = inlet_pressure * self.compression_ratio

        fluid = Fluid(FluidsList.Air).with_state(
            Input.pressure(inlet_pressure),
            Input.temperature(inlet_temperature),
        )

        return fluid.compression_to_pressure(
            pressure=outlet_pressure,
            isentropic_efficiency=self.efficiency * 100,
        )


class GasCombustionChamber(Device):
    """
    Represents a gas combustion chamber in a thermodynamic cycle.

    Attributes:
    outlet_temperature (float): The temperature of the gas at the outlet of
        the combustion chamber (C).

    Methods:
    __init__: Initializes a new instance of the CombustionChamber class.
    """

    def __init__(
        self,
        name: str,
        outlet_temperature: float,
    ) -> None:
        """
        Initializes a new instance of the GasCombustionChamber class.

        Parameters:
        name (str): The name or identifier of the combustion chamber.
        outlet_temperature (float): The temperature of the gas at the outlet
            of the combustion chamber (in C).
        """
        super().__init__(name)
        self.outlet_temperature = outlet_temperature

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        pressure = inlet_state.pressure

        fluid = Fluid(FluidsList.Air).with_state(
            Input.pressure(pressure),
            Input.temperature(self.outlet_temperature),
        )

        return fluid


class GasTurbine(NonIsentropicDevice):
    """
    Represents a gas turbine in a thermodynamic cycle.

    Attributes:
    outlet_pressure (float): The pressure of the gas at the outlet of the turbine (in Pascals).

    Methods:
    __init__: Initializes a new instance of the GasTurbine class.
    """

    def __init__(
        self,
        name: str,
        efficiency: float,
        outlet_pressure: float,
    ) -> None:
        """
        Initializes a new instance of the GasTurbine class.

        Parameters:
        name (str): The name or identifier of the gas turbine.
        efficiency (float): The efficiency of the turbine (as a decimal).
        outlet_pressure (float): The pressure of the gas at the outlet of the turbine (in Pascals).
        """
        super().__init__(name, efficiency)
        self.outlet_pressure = outlet_pressure

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        inlet_pressure = inlet_state.pressure
        inlet_temperature = inlet_state.temperature

        fluid = Fluid(FluidsList.Air).with_state(
            Input.pressure(inlet_pressure),
            Input.temperature(inlet_temperature),
        )

        return fluid.expansion_to_pressure(
            pressure=self.outlet_pressure,
            isentropic_efficiency=self.efficiency * 100,
        )
