"""
Module for plotting functions.
"""

import numpy as np
import plotly.graph_objs as go
from pyfluids import Fluid, Input

from thermosys.services.units import bar_to_pascal, pascal_to_bar


def plot_saturation_curve(fluid: Fluid, fig: go.Figure | None = None):
    """
    Plots the saturation curve on the temperature-entropy diagram for a given fluid.

    Args:
    fluid (Fluid): Fluid for which the TS diagram is plotted.
    fig (plotly.graph_objs.Figure | None): An existing figure to add the TS plot to. Defaults to None.

    Returns:
    plotly.graph_objs.Figure: A Plotly figure object with the saturation curve.
    """

    # Calculate temperatures for the saturation curve:
    min_temperature = fluid.min_temperature
    max_temperature = fluid.critical_temperature
    temperatures = np.linspace(min_temperature + 0.01, max_temperature - 0.01)

    # Calculate saturation entropy values:
    s_vapor = np.array(
        [fluid.dew_point_at_temperature(t).entropy for t in temperatures]
    )
    s_liquid = np.array(
        [
            fluid.with_state(Input.temperature(t), Input.quality(0)).entropy
            for t in temperatures
        ]
    )
    entropy = np.concatenate((s_liquid, s_vapor[::-1]))
    temp_combined = np.concatenate((temperatures, temperatures[::-1]))

    # Create the saturation curve trace
    saturation_trace = go.Scatter(
        name=f"Saturation - {fluid.name.value}",
        x=entropy * 1e-3,
        y=temp_combined,
        line={"color": "black"},
    )

    # Update figure with the saturation curve
    if fig is None:
        fig = go.Figure()

    fig.add_trace(saturation_trace)
    fig.update_layout(
        yaxis={"title": "Temperature [°C]"},
        xaxis={"title": "Specific Entropy [kJ/kg/K]"},
        title="Temperature-Entropy Diagram",
    )

    return fig


def add_isobaric_process_to_plot(
    fluid: Fluid,
    pressure: float,
    fig: go.Figure,
    min_temp: float = 0,
    max_temp: float = 1200,
    line_style: dict = {"color": "blue"},
    num_points: int = 500,
) -> go.Figure:
    """
    Adds an isobaric process curve to a temperature-entropy (TS) plot.

    Returns:
    go.Figure: The updated Plotly figure.
    """

    min_entropy = fluid.with_state(
        Input.temperature(min_temp),
        Input.pressure(pressure),
    ).entropy
    max_entropy = fluid.with_state(
        Input.temperature(max_temp),
        Input.pressure(pressure),
    ).entropy

    entropy_values = np.linspace(min_entropy, max_entropy, num_points)

    # Calculate temperatures:
    temperatures = np.array(
        [
            fluid.with_state(
                Input.pressure(pressure), Input.entropy(entropy)
            ).temperature
            for entropy in entropy_values
        ]
    )

    # Add the isobaric process trace:
    trace = go.Scatter(
        name=f"P = {pascal_to_bar(pressure):.2f} bar",
        x=entropy_values * 1e-3,  # Convert to kJ/kg/K
        y=temperatures,
        line=line_style,
        connectgaps=True,
    )
    fig.add_trace(trace)

    return fig


def mark_state_ts(state: Fluid, fig: go.Figure):
    ps = go.Scatter(
        x=[state.entropy * 1e-3],
        y=[state.temperature],
        mode="markers",
        marker={"color": "red"},
    )

    fig.add_trace(ps)


def plot_isobaric_process(
    state_1: Fluid,
    state_2: Fluid,
    fig,
    style={"color": "black"},
    num_points=200,
):
    """
    Plots an isobaric process between two states on a TS diagram.
    """
    assert state_1.pressure == state_2.pressure, "Pressures must be identical."

    entropy = np.linspace(state_1.entropy, state_2.entropy, num_points)
    temperature = np.array(
        [
            state_1.with_state(
                Input.entropy(s), Input.pressure(state_1.pressure)
            ).temperature
            for s in entropy
        ]
    )

    trace = go.Scatter(
        x=entropy * 1e-3,
        y=temperature,
        line=style,
        showlegend=False,
    )

    fig.add_trace(trace)


def plot_expansion_process(
    state_1: Fluid,
    state_2: Fluid,
    isentropic_efficiency: float,
    fig,
    style={"color": "black"},
    num_points=20,
):
    """
    Plots an expansion process between two states with a given isentropic efficiency.
    """

    def calculate_expansion_enthalpy(pressure):
        """Calculate enthalpy for expansion at a given pressure."""
        h2s = state_1.with_state(
            Input.pressure(pressure), Input.entropy(state_1.entropy)
        ).enthalpy
        h2 = state_1.enthalpy - isentropic_efficiency * (
            state_1.enthalpy - h2s
        )
        return h2

    pressures = np.linspace(state_1.pressure, state_2.pressure, num_points)
    enthalpies = np.array([calculate_expansion_enthalpy(p) for p in pressures])
    entropies = np.array(
        [
            state_1.with_state(Input.pressure(p), Input.enthalpy(h)).entropy
            for p, h in zip(pressures, enthalpies)
        ]
    )
    temperatures = np.array(
        [
            state_1.with_state(
                Input.pressure(p), Input.enthalpy(h)
            ).temperature
            for p, h in zip(pressures, enthalpies)
        ]
    )

    trace = go.Scatter(
        x=entropies * 1e-3,
        y=temperatures,
        line=style,
        showlegend=False,
    )

    fig.add_trace(trace)


def plot_compression_process(
    state_1: Fluid,
    state_2: Fluid,
    isentropic_efficiency: float,
    fig,
    style={"color": "black"},
    num_points=20,
):
    """
    Plots a compression process between two states with a given isentropic efficiency.
    """

    def calculate_compression_enthalpy(pressure):
        """Calculate enthalpy for compression at a given pressure."""
        h2s = state_1.with_state(
            Input.pressure(pressure), Input.entropy(state_1.entropy)
        ).enthalpy
        h2 = (
            state_1.enthalpy + (h2s - state_1.enthalpy) / isentropic_efficiency
        )
        return h2

    pressures = np.linspace(state_1.pressure, state_2.pressure, num_points)
    enthalpies = np.array(
        [calculate_compression_enthalpy(p) for p in pressures]
    )
    entropies = np.array(
        [
            state_1.with_state(Input.pressure(p), Input.enthalpy(h)).entropy
            for p, h in zip(pressures, enthalpies)
        ]
    )
    temperatures = np.array(
        [
            state_1.with_state(
                Input.pressure(p), Input.enthalpy(h)
            ).temperature
            for p, h in zip(pressures, enthalpies)
        ]
    )

    trace = go.Scatter(
        x=entropies * 1e-3,
        y=temperatures,
        line=style,
        showlegend=False,
    )

    fig.add_trace(trace)


def plot_isoenthalpic_process(
    state_1: Fluid,
    state_2: Fluid,
    fig,
    style={"color": "black", "dash": "dot"},
    num_points=20,
):
    """
    Plots an isoenthalpic process between two states on a TS diagram.
    """

    assert (
        abs(state_1.enthalpy - state_2.enthalpy) < 1e-4
    ), "Enthalpies must be identical."

    entropy_values = np.linspace(state_1.entropy, state_2.entropy, num_points)
    temperatures = np.array(
        [
            state_1.fluid.with_state(
                Input.entropy(s), Input.enthalpy(state_1.enthalpy)
            ).temperature
            for s in entropy_values
        ]
    )

    trace = go.Scatter(
        x=entropy_values * 1e-3,
        y=temperatures,
        line=style,
        showlegend=False,
    )

    fig.add_trace(trace)
