"""
Classes that represent thermodynamic cycles.
"""

from abc import ABC, abstractmethod

import numpy as np
from pyfluids import Fluid


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

        self.devices = []
        self.states = []

    @abstractmethod
    def get_efficiency(self) -> float:
        """
        Returns the efficiency of the cycle.

        Returns:
        float: The efficiency of the cycle (as a decimal).
        """
        if len(self.states) < 2:
            raise ValueError(
                "The cycle must be solved before getting its efficiency."
            )

    @abstractmethod
    def print_results(self) -> None:
        """
        Prints the results of the cycle.
        """
        for i, state in enumerate(self.states):
            print(
                f"{i+1} - {state.name}: {state.pressure * 1e-5:.2f} bar, {state.temperature:.2f} C, {state.enthalpy * 1e-3:.2f} kJ/kg"
            )

        print("\n")

        for device in self.devices:
            print(
                f"{device.name}: {device.energy_balance * 1e-3:.2f} kJ/kg",
            )

        print("\n")

        print(f"Efficiency: {self.get_efficiency() * 100:.2f} %")

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
    def heat_in(self) -> float:
        """
        Returns the heat added to the cycle.

        Returns:
        float: The heat added to the cycle (J/kg).
        """
        heat_in = np.sum(
            device.energy_balance
            for device in self.devices
            if device.device_type == "heat_source"
        )

        return heat_in


class BraytonCycle(ThermodynamicCycle):
    """
    Represents a Brayton cycle in a thermodynamic system.
    """

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

    def get_efficiency(self) -> float:
        super().get_efficiency()
        return (self.turbine_work - self.compressor_work) / self.heat_in

    def print_results(self) -> None:
        """
        Prints the results of the cycle.
        """
        print("BRAYTON CYCLE RESULTS\n")

        super().print_results()

        print("\n")

        print(f"Turbine work: {self.turbine_work * 1e-3:.2f} kJ/kg")
        print(f"Compressor work: {self.compressor_work * 1e-3:.2f} kJ/kg")
        print(
            f"Total work: {(self.turbine_work - self.compressor_work) * 1e-3:.2f} kJ/kg"
        )
        print(f"Heat input: {self.heat_in * 1e-3:.2f} kJ/kg")
