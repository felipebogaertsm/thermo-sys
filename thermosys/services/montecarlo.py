import numpy as np
import plotly.graph_objects as go


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


import plotly.express as px


def plot_monte_carlo(array_1: np.ndarray, array_2: np.ndarray):
    """
    Plot a Monte Carlo simulation result showing the relationship between pressure and efficiency using Plotly.

    Parameters:
    array_1 (np.ndarray): Array of pressure values.
    array_2 (np.ndarray): Array of efficiency values corresponding to the array_1.
    """
    if array_1.shape != array_2.shape:
        raise ValueError("The shapes of array_1 and array_2 must be the same.")

    fig = go.Figure(data=go.Scatter(x=array_1, y=array_2, mode="markers"))
    fig.update_layout(
        title="Monte Carlo Simulation: Pressure vs Efficiency",
        xaxis_title="Pressure",
        yaxis_title="Efficiency",
    )
    fig.show()
