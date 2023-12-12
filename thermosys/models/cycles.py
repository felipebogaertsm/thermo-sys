"""
Classes that represent thermodynamic cycles.
"""

from abc import ABC, abstractmethod

import numpy as np
from pyfluids import Fluid

from thermosys.models.devices import Device


class ThermodynamicCycle(ABC):
    """
    Represents a Thermodynamic Cycle. A cycle is composed of a sequence of
    processes and defined states between them.

    Attributes:
    initial_state (Fluid): The initial state of the gas in the system.
    mass_flux (float): The mass flux of the system.
    devices (list): A list of devices (e.g., compressors, turbines) in the cycle.

    Methods:
    __init__: Initializes a new instance of the class.
    add_device: Adds a new device to the cycle.
    solve: Solves for the states of the cycle.
    """

    def __init__(
        self,
        initial_state: Fluid,
        mass_flux: float,
    ) -> None:
        """
        Initializes a new instance of the BraytonCycle class with an empty list of devices.

        Parameters:
        initial_state (Fluid): The initial state of the gas in the system.
        mass_flux (float): The mass flux of the system (kg/s)
        """
        self.initial_state = initial_state
        self.mass_flux = mass_flux

        self.devices = []  # filled in by add_device method
        self.states = []  # filled in by solve method

    def add_device(self, device: Device) -> None:
        """
        Adds a new device to the cycle.

        Parameters:
        device (Device): The device to be added to the cycle.
        """
        self.devices.append(device)

    def solve(self) -> None:
        """
        Solves for the states at different points in the cycle.

        This method should implement the necessary calculations to determine the thermodynamic
        states at various points in the cycle, based on the characteristics of the devices
        in the cycle. The implementation will depend on the specifics of the Brayton cycle
        and the data available from each device.
        """
        self.states = [self.initial_state]  # clear any previous states

        for i, device in enumerate(self.devices):
            inlet_state = self.states[i]
            device.inlet_state = inlet_state

            self.states.append(
                device.get_outlet_state(inlet_state=inlet_state)
            )

    @abstractmethod
    def get_efficiency(self) -> float:
        """
        Returns the efficiency of the cycle. Cycle must have been solved
        before calling this method.

        Returns:
        float: The efficiency of the cycle (as a decimal).
        """
        if len(self.states) < 2:
            raise ValueError(
                "The cycle must be solved before getting its efficiency."
            )


class BraytonCycle(ThermodynamicCycle):
    """
    Represents a Brayton cycle in a thermodynamic system.
    """

    @property
    def turbine_work(self) -> float:
        """
        Returns the work done by the turbine in the cycle.

        Returns:
        float: The work done by the turbine (J/kg).
        """
        turbine_work = np.sum(
            device.energy_balance
            for device in self.devices
            if device.device_type == "turbine"
        )

        return turbine_work

    @property
    def compressor_work(self) -> float:
        """
        Returns the work done by the compressor in the cycle.

        Returns:
        float: The work done by the compressor (J/kg).
        """
        compressor_work = np.sum(
            device.energy_balance
            for device in self.devices
            if device.device_type == "compressor"
        )

        return compressor_work

    @property
    def heat_in(self) -> float:
        """
        Returns the heat added to the cycle.

        Returns:
        float: The heat added to the cycle (J/kg).
        """
        heat_in = np.sum(
            device.energy_balance
            for device in self.devices
            if device.device_type == "combustion_chamber"
        )

        return heat_in

    def get_efficiency(self) -> float:
        super().get_efficiency()
        return (self.turbine_work - self.compressor_work) / self.heat_in
