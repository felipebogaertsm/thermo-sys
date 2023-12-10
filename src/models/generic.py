from dataclasses import dataclass


@dataclass
class State:
    """
    Represents the thermodynamic state of a system.

    Attributes:
    temperature (float): Temperature of the state (in Kelvin, unless otherwise noted).
    pressure (float): Pressure of the state (in Pascals).
    enthalpy (float): Enthalpy of the state (in Joules per kilogram).
    entropy (float): Entropy of the state (in Joules per kilogram per Kelvin).
    specific_volume (float): Specific volume of the state (in cubic meters per kilogram).
    """

    temperature: float
    pressure: float
    enthalpy: float
    entropy: float
    specific_volume: float
