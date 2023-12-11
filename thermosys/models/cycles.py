"""
Classes that represent thermodynamic cycles.
"""

from abc import ABC, abstractmethod
from thermosys.models.devices import Device


class ThermodynamicCycle(ABC):
    """
    Represents a Thermodynamic Cycle. A cycle is composed of a sequence of
    processes and defined states between them.

    Methods:
    __init__: Initializes a new instance of the ThermodynamicCycle class.
    """

    @abstractmethod
    def add_device(self, device: Device) -> None:
        """
        Adds a new device to the cycle.

        Parameters:
        device (Device): The device to be added to the cycle.
        """

    @abstractmethod
    def solve(self) -> None:
        """
        Solves for the states of the cycle.

        This method should implement the necessary calculations to determine the thermodynamic
        states at various points in the cycle.
        """


class BraytonCycle(ThermodynamicCycle):
    """
    Represents a Brayton cycle in a thermodynamic system.

    Attributes:
    ambient_temperature (float): The ambient temperature of the system.
    ambient_pressure (float): The ambient pressure of the system.
    mass_flux (float): The mass flux of the system.
    devices (list): A list of devices (e.g., compressors, turbines) in the cycle.

    Methods:
    __init__: Initializes a new instance of the BraytonCycle class.
    add_device: Adds a new device to the cycle.
    solve: Solves for the states of the cycle.
    """

    def __init__(
        self,
        ambient_temperature: float,
        ambient_pressure: float,
        mass_flux: float,
    ) -> None:
        """
        Initializes a new instance of the BraytonCycle class with an empty list of devices.

        Parameters:
        ambient_temperature (float): The ambient temperature of the system (C).
        ambient_pressure (float): The ambient pressure of the system (Pa).
        mass_flux (float): The mass flux of the system (kg/s)
        """
        self.ambient_temperature = ambient_temperature
        self.ambient_pressure = ambient_pressure
        self.mass_flux = mass_flux

        self.devices = []  # filled in by add_device method
        self.states = []  # filled in by solve method

    def add_device(self, device: Device) -> None:
        """
        Adds a new device to the Brayton cycle.

        Parameters:
        device (Device): The device to be added to the cycle.
        """
        self.devices.append(device)

    def solve(self) -> None:
        """
        Solves for the states at different points in the Brayton cycle.

        This method should implement the necessary calculations to determine the thermodynamic
        states at various points in the cycle, based on the characteristics of the devices
        in the cycle. The implementation will depend on the specifics of the Brayton cycle
        and the data available from each device.
        """
        self.states = []  # clear any previous states

        for device in self.devices:
            self.states.append(device.get_outlet_state())
