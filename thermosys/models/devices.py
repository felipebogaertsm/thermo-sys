"""
Defines classes that represent devices in a thermodynamic cycle.
These classes are generally behavioral, so regular classes instead of 
dataclasses will be used.
"""

from abc import ABC, abstractmethod, abstractproperty

import numpy as np
from pyfluids import Fluid, FluidsList, Input


class Device(ABC):
    """
    Represents a general device in a thermodynamic cycle.

    Attributes:
    name (str): The name or identifier of the device.

    Methods:
    __init__: Initializes a new instance of the Device class.
    device_type: Returns the type of the device.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the Device class.

        Parameters:
        name (str): The name or identifier of the device.
        """
        self.name = name

    @abstractproperty
    def device_type(self) -> str:
        """
        Returns the type of the device.

        Returns:
        str: The type of the device (e.g., "compressor", "turbine", "heat_source").
        """


class SingleInletOutletDevice(Device):
    """
    Represents a general device in a thermodynamic cycle with a single inlet
    and single outlet.

    Attributes:
    inlet_state (Fluid | None): The state of the gas at the inlet of the
        device.
    outlet_state (Fluid | None): The state of the gas at the outlet of the
        device.

    Methods:
    __init__: Initializes a new instance of the SingleInletOutletDevice class.
    get_outlet_state: Returns the state of the gas at the outlet of the device.
    energy_balance: Returns the energy balance of the device.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the SingleInletOutletDevice class.
        """
        super().__init__(name)

        self.inlet_state = None
        self.outlet_state = None

    @abstractmethod
    def get_outlet_state(self, inlet_state: Fluid, *args, **kwargs) -> Fluid:
        """
        Returns the state of the gas at the outlet of the device.

        Parameters:
        inlet_state (Fluid): The state of the gas at the inlet of the device.

        Returns:
        Fluid: The state of the gas at the outlet of the device.
        """
        self.inlet_state = inlet_state

    @property
    def energy_balance(self) -> float:
        """
        Returns the energy balance of the device.

        Returns:
        float: The energy balance of the device (J/kg).
        """
        if self.inlet_state is None or self.outlet_state is None:
            raise ValueError("The inlet and outlet states must be defined.")

        return np.abs(self.outlet_state.enthalpy - self.inlet_state.enthalpy)


class NonIsentropicDevice(SingleInletOutletDevice):
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
        self, name: str, efficiency: float, compression_ratio: float
    ) -> None:
        """
        Initializes a new instance of the GasCompressor class.

        Parameters:
        name (str): The name or identifier of the compressor.
        efficiency (float): The efficiency of the compressor (as a decimal).
        compression_ratio (float | None): The ratio of the outlet pressure to the inlet pressure.
        """
        super().__init__(name, efficiency)
        self.compression_ratio = compression_ratio

    @property
    def device_type(self) -> str:
        return "compressor"

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        super().get_outlet_state(inlet_state)

        inlet_pressure = inlet_state.pressure
        inlet_temperature = inlet_state.temperature

        outlet_pressure = inlet_pressure * self.compression_ratio

        fluid = Fluid(FluidsList.Air).with_state(
            Input.pressure(inlet_pressure),
            Input.temperature(inlet_temperature),
        )

        self.outlet_state = fluid.compression_to_pressure(
            pressure=outlet_pressure,
            isentropic_efficiency=self.efficiency * 100,
        )
        return self.outlet_state


class HeatSourceDevice(SingleInletOutletDevice):
    """
    Represents a heat source in a thermodynamic cycle, capable of using different types of fluids.

    Attributes:
    fluid_type (FluidsList): The type of fluid used in the device.
    outlet_temperature (float): The temperature of the fluid at the outlet of the heat source (in °C).

    Methods:
    __init__: Initializes a new instance of the HeatSourceDevice class.
    """

    def __init__(
        self,
        name: str,
        fluid_type: FluidsList,
        outlet_temperature: float,
    ) -> None:
        """
        Initializes a new instance of the HeatSourceDevice class.

        Parameters:
        name (str): The name or identifier of the heat source.
        fluid_type (FluidsList): The type of fluid used in the device.
        outlet_temperature (float): The temperature of the fluid at the outlet of the heat source (in °C).
        """
        super().__init__(name)
        self.fluid_type = fluid_type
        self.outlet_temperature = outlet_temperature

    @property
    def device_type(self) -> str:
        return "heat_source"

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        super().get_outlet_state(inlet_state)

        # Use the specified fluid type for setting the state
        fluid = Fluid(self.fluid_type).with_state(
            Input.pressure(inlet_state.pressure),
            Input.temperature(self.outlet_temperature),
        )

        self.outlet_state = fluid
        return self.outlet_state


class Turbine(NonIsentropicDevice):
    """
    Represents a gas turbine in a thermodynamic cycle, capable of using different types of fluids.

    Attributes:
    fluid_type (FluidsList): The type of fluid used in the turbine.
    outlet_pressure (float): The pressure of the gas at the outlet of the turbine (in Pascals).

    Methods:
    __init__: Initializes a new instance of the GasTurbine class.
    """

    def __init__(
        self,
        name: str,
        efficiency: float,
        fluid_type: FluidsList,
        outlet_pressure: float,
    ) -> None:
        """
        Initializes a new instance of the GasTurbine class.

        Parameters:
        name (str): The name or identifier of the gas turbine.
        efficiency (float): The efficiency of the turbine (as a decimal).
        fluid_type (FluidsList): The type of fluid used in the turbine.
        outlet_pressure (float): The pressure of the gas at the outlet of the turbine (in Pascals).
        """
        super().__init__(name, efficiency)
        self.fluid_type = fluid_type
        self.outlet_pressure = outlet_pressure

    @property
    def device_type(self) -> str:
        return "turbine"

    def get_outlet_state(
        self, inlet_state: Fluid, energy_balance: float | None = None
    ) -> Fluid:
        super().get_outlet_state(inlet_state)

        # Create a new fluid instance using the specified fluid type
        fluid = Fluid(self.fluid_type).with_state(
            Input.pressure(inlet_state.pressure),
            Input.temperature(inlet_state.temperature),
        )

        if energy_balance is not None:
            outlet_enthalpy = (
                inlet_state.enthalpy - energy_balance / self.efficiency
            )

            pressure_drop = np.abs(inlet_state.pressure - self.outlet_pressure)

            self.outlet_state = fluid.cooling_to_enthalpy(
                enthalpy=outlet_enthalpy, pressure_drop=pressure_drop
            )
        else:
            self.outlet_state = fluid.expansion_to_pressure(
                pressure=self.outlet_pressure,
                isentropic_efficiency=self.efficiency * 100,
            )

        return self.outlet_state


class Condenser(SingleInletOutletDevice):
    """
    Represents a condenser in a thermodynamic cycle.

    Attributes:
    pressure (float): The pressure of the fluid at the outlet of the condenser (in Pascals).

    Methods:
    __init__: Initializes a new instance of the Condenser class.
    """

    def __init__(
        self,
        name: str,
        fluid_type: FluidsList,
        pressure: float,
    ) -> None:
        """
        Initializes a new instance of the Condenser class.

        Parameters:
        name (str): The name or identifier of the condenser.
        fluid_type (FluidsList): The type of fluid used in the condenser.
        pressure (float): The pressure of the fluid at the outlet of the condenser (in Pascals).
        """
        super().__init__(name)
        self.fluid_type = fluid_type
        self.pressure = pressure

    @property
    def device_type(self) -> str:
        return "condenser"

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        super().get_outlet_state(inlet_state)

        # Create a new fluid instance using the specified fluid type
        fluid = Fluid(self.fluid_type)

        # Saturation fluid (x = 0)
        saturated_fluid = fluid.dew_point_at_pressure(pressure=self.pressure)

        self.outlet_state = saturated_fluid
        return self.outlet_state


class Pump(NonIsentropicDevice):
    """
    Represents a water pump in a thermodynamic cycle.

    Attributes:
    outlet_pressure (float): The pressure of the water at the outlet of the pump (in Pascals).

    Methods:
    __init__: Initializes a new instance of the Pump class.
    """

    def __init__(
        self, name: str, efficiency: float, outlet_pressure: float
    ) -> None:
        """
        Initializes a new instance of the Pump class.

        Parameters:
        name (str): The name or identifier of the pump.
        efficiency (float): The efficiency of the pump (as a decimal).
        outlet_pressure (float): The pressure of the water at the outlet of the pump (in Pascals).
        """
        super().__init__(name, efficiency)
        self.outlet_pressure = outlet_pressure

    @property
    def device_type(self) -> str:
        return "pump"

    def get_outlet_state(self, inlet_state: Fluid) -> Fluid:
        super().get_outlet_state(inlet_state)

        self.outlet_state = inlet_state.compression_to_pressure(
            pressure=self.outlet_pressure,
            isentropic_efficiency=self.efficiency * 100,
        )

        return self.outlet_state

    def get_inlet_state(
        self, outlet_state: Fluid, inlet_pressure: float
    ) -> Fluid:
        """
        Determines the inlet state for the pump based on the outlet state.

        Parameters:
        outlet_state (Fluid): The known outlet state of the pump.
        inlet_pressure (float): The pressure of the water at the inlet of the pump (in Pascals).

        Returns:
        Fluid: The calculated inlet state for the pump.
        """
        self.outlet_state = outlet_state

        self.inlet_state = outlet_state.expansion_to_pressure(
            pressure=inlet_pressure,
            isentropic_efficiency=self.efficiency * 100,
        )

        return self.inlet_state


class Deaerator(Device):
    """
    Represents a deaerator in a thermodynamic cycle.

    Attributes:
    temperature (float): The temperature of the deaerator (in °C), which is crucial for the deaeration process.

    Methods:
    __init__: Initializes a new instance of the Deaerator class.
    """

    def __init__(self, name: str, temperature: float) -> None:
        """
        Initializes a new instance of the Deaerator class.

        Parameters:
        name (str): The name or identifier of the deaerator.
        temperature (float): The operating temperature of the deaerator (in °C).
        """
        super().__init__(name)
        self.temperature = temperature

    @property
    def device_type(self) -> str:
        return "deaerator"
