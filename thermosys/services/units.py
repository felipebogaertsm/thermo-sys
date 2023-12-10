def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert temperature from Celsius to Fahrenheit.

    Parameters:
    celsius (float): Temperature in degrees Celsius.

    Returns:
    float: Temperature in degrees Fahrenheit.
    """
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert temperature from Fahrenheit to Celsius.

    Parameters:
    fahrenheit (float): Temperature in degrees Fahrenheit.

    Returns:
    float: Temperature in degrees Celsius.
    """
    return (fahrenheit - 32) * 5 / 9


def kelvin_to_celsius(kelvin: float) -> float:
    """
    Convert temperature from Kelvin to Celsius.

    Parameters:
    kelvin (float): Temperature in Kelvin.

    Returns:
    float: Temperature in degrees Celsius.
    """
    return kelvin - 273.15


def celsius_to_kelvin(celsius: float) -> float:
    """
    Convert temperature from Celsius to Kelvin.

    Parameters:
    celsius (float): Temperature in degrees Celsius.

    Returns:
    float: Temperature in Kelvin.
    """
    return celsius + 273.15


def atm_to_pascal(atm: float) -> float:
    """
    Convert pressure from atmospheres to Pascals.

    Parameters:
    atm (float): Pressure in atmospheres.

    Returns:
    float: Pressure in Pascals.
    """
    return atm * 101325


def bar_to_pascal(bar: float) -> float:
    """
    Convert pressure from bar to Pascals.

    Parameters:
    bar (float): Pressure in bar.

    Returns:
    float: Pressure in Pascals.
    """
    return bar * 100000


def liter_to_cubic_meter(liters: float) -> float:
    """
    Convert volume from liters to cubic meters.

    Parameters:
    liters (float): Volume in liters.

    Returns:
    float: Volume in cubic meters.
    """
    return liters / 1000


def gallon_to_liter(gallons: float) -> float:
    """
    Convert volume from gallons to liters.

    Parameters:
    gallons (float): Volume in gallons.

    Returns:
    float: Volume in liters.
    """
    return gallons * 3.78541


def joule_to_btu(joules: float) -> float:
    """
    Convert energy from Joules to British Thermal Units (BTUs).

    Parameters:
    joules (float): Energy in Joules.

    Returns:
    float: Energy in BTUs.
    """
    return joules * 0.000947817


def kwh_to_joule(kwh: float) -> float:
    """
    Convert energy from kilowatt-hours to Joules.

    Parameters:
    kwh (float): Energy in kilowatt-hours.

    Returns:
    float: Energy in Joules.
    """
    return kwh * 3600000
