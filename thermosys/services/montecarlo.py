import numpy as np


def get_random_value(min_value: float, max_value: float) -> float:
    """
    Generates a random value within a specified range using numpy.

    Parameters:
    min_value (float): The minimum value in the range.
    max_value (float): The maximum value in the range.

    Returns:
    float: A random value within the specified range.
    """
    return np.random.uniform(min_value, max_value)
