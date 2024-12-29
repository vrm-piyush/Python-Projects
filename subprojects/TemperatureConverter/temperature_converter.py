# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Temperature Converter Program.

Input:
- Temperature value.
- Unit of temperature to convert from (F, C, K, R, DE, N).
- Unit of temperature to convert to (F, C, K, R, DE, N).
- Precision (number of decimal places).

Output:
- Converted temperature value in the specified unit.
- Graphical representation of the temperature value on different scales.

Features:
- Converts temperature values between Fahrenheit (F), Celsius (C), Kelvin (K), Rankine (R), Delisle (DE), and Newton (N) units.
- Graphically represents the temperature value on different scales using Matplotlib.
- Validates temperature input against specified ranges for each unit.
- Handles exceptions for invalid input and conversion errors.
- Supports customizable precision for the converted temperature values.
- Includes a sample temperature conversion graph for reference.
- Allows users to visualize temperature values on different scales for comparison.
- Displays the converted temperature value with the specified precision.
- Handles non-numeric input and other exceptions gracefully.
- Provides a simple and intuitive command-line interface for users to interact with the program.

"""

import matplotlib.pyplot as plt
import numpy as np

def plot_temperature_graph(value: float, from_unit: str):
    """
    Plot a graphical representation (chart or graph) of temperature values on different scales.

    Args:
    - value (float): Temperature value to plot.
    - from_unit (str): Unit of temperature to convert from (F, C, K, R, DE, N, etc.).
    """

    temperature_scales = ['F', 'C', 'K', 'R', 'DE', 'N']

    temperatures = [convert_temperature(value, from_unit, to_unit) for to_unit in temperature_scales]

    temperature_scales_array = np.array(temperature_scales)  # Convert temperature scales to an array-like object
    temperatures_array = np.array(temperatures)  # Convert temperatures to an array-like object

    fig, ax = plt.subplots()
    bars = ax.bar(temperature_scales_array, temperatures_array)

    # Add individual values as text annotations on top of each bar
    for bar, temp in zip(bars, temperatures):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f'{temp:.2f}', ha='center')

    plt.title(f'Temperature Conversion from {from_unit.upper()} to Different Scales')
    plt.xlabel('Temperature Scales')
    plt.ylabel('Temperature Values')
    plt.show()

def is_valid_temperature(value: float, unit: str) -> bool:
    """
    Check if the entered temperature value is within a valid range for the specified unit.

    Args:
    - value (float): Temperature value to check.
    - unit (str): Unit of temperature (F, C, K, etc.).

    Returns:
    - bool: True if the temperature is within a valid range, False otherwise.
    """

    temperature_ranges = {
        'F': {'min': -459.67, 'max': float('inf')},     # Absolute zero in Fahrenheit
        'C': {'min': -273.15, 'max': float('inf')},     # Absolute zero in Celsius
        'K': {'min': 0, 'max': float('inf')},           # Absolute zero in Kelvin
        'R': {'min': 0, 'max': float('inf')},           # Rankine scale
        'DE': {'min': -559.725, 'max': float('inf')},   # Delisle scale
        'N': {'min': -90.139, 'max': 90}                # Newton scale
        # Add more temperature unit ranges as needed
    }

    unit_upper = unit.upper()
    if unit_upper in temperature_ranges:
        temperature_range = temperature_ranges[unit_upper]
        return temperature_range['min'] <= value <= temperature_range['max']
    else:
        raise ValueError(f"Unsupported temperature unit: {unit}")


def convert_temperature(value: float, from_unit: str, to_unit: str, precision: int = 2) -> float:
    """
    Convert temperature between Fahrenheit, Celsius, Kelvin, Rankine, Delisle, and Newton units.
    
    Args:
    - value (float): Temperature value to convert.
    - from_unit (str): Unit of temperature to convert from (F, C, K, R, DE, N, etc.).
    - to_unit (str): Unit of temperature to convert to (F, C, K, R, DE, N, etc.).
    - precision (int): Number of decimal places for the result.
    
    Returns:
    - float: Converted temperature value.
    """

    if not is_valid_temperature(value, from_unit):
        raise ValueError(f"Invalid temperature value {value} for unit {from_unit}")

    conversion_result = 0.0

    if from_unit.lower() == 'f':
        if to_unit.lower() == 'c':
            conversion_result =  (value - 32) * 5/9
        elif to_unit.lower() == 'k':
            conversion_result =  (value - 32) * 5/9 + 273.15
        elif to_unit.lower() == 'r':
            conversion_result =  value + 459.67
        elif to_unit.lower() == 'de':
            conversion_result =  (212 - value) * 5/6
        elif to_unit.lower() == 'n':
            conversion_result =  (value - 32) * 11/60
    elif from_unit.lower() == 'c':
        if to_unit.lower() == 'f':
            conversion_result =  (value * 9/5) + 32
        elif to_unit.lower() == 'k':
            conversion_result =  value + 273.15
        elif to_unit.lower() == 'r':
            conversion_result =  (value * 9/5) + 491.67
        elif to_unit.lower() == 'de':
            conversion_result =  (100 - value) * (2 / 3)
        elif to_unit.lower() == 'n':
            conversion_result =  value * 33/100
    elif from_unit.lower() == 'k':
        if to_unit.lower() == 'c':
            conversion_result =  value - 273.15
        elif to_unit.lower() == 'f':
            conversion_result =  (value - 273.15) * 9/5 + 32
        elif to_unit.lower() == 'r':
            conversion_result =  value * 9/5
        elif to_unit.lower() == 'de':
            conversion_result =  (373.15 - value) * 3/2
        elif to_unit.lower() == 'n':
            conversion_result =  (value - 273.15) * 33/100
    elif from_unit.lower() == 'r':
        if to_unit.lower() == 'f':
            conversion_result =  value - 459.67
        elif to_unit.lower() == 'c':
            conversion_result =  (value - 491.67) * 5/9
        elif to_unit.lower() == 'k':
            conversion_result =  value * 5/9
        elif to_unit.lower() == 'de':
            conversion_result =  (671.67 - value) * 5/6
        elif to_unit.lower() == 'n':
            conversion_result =  (value - 491.67) * 11/60
    elif from_unit.lower() == 'de':
        if to_unit.lower() == 'f':
            conversion_result =  212 - (value * 6/5)
        elif to_unit.lower() == 'c':
            conversion_result =  100 - (value * 3/2)
        elif to_unit.lower() == 'k':
            conversion_result =  373.15 - (value * 2/3)
        elif to_unit.lower() == 'r':
            conversion_result =  671.67 - (value * 5/6)
        elif to_unit.lower() == 'n':
            conversion_result =  33 - (value * 50/11)
    elif from_unit.lower() == 'n':
        if to_unit.lower() == 'f':
            conversion_result =  (value * 60/11) + 491.67
        elif to_unit.lower() == 'c':
            conversion_result =  value * 100/33
        elif to_unit.lower() == 'k':
            conversion_result =  (value * 100/33) + 273.15
        elif to_unit.lower() == 'r':
            conversion_result =  (value * 60/11) + 491.67
        elif to_unit.lower() == 'de':
            conversion_result =  33 - (value * 50/11)

    return round(conversion_result, precision)  # If the conversion units are the same, return the value as is


if __name__ == '__main__':
    try:
        # Prompt the user to enter the temperature value and units for conversion.
        value = float(input("Enter the temperature value: "))
        from_unit = input("Enter the unit of temperature to convert from (F, C, K, R, DE, N.): ").strip()
        to_unit = input("Enter the unit of temperature to convert to (F, C, K, R, DE, N.): ").strip()
        precision = int(input("Enter the precision (number of decimal places): ").strip())

        # Convert the temperature value to the desired unit.
        converted_value = convert_temperature(value, from_unit, to_unit, precision)

        # Display the converted temperature value to the user.
        print(f'{value} {from_unit.upper()} is equal to {converted_value:.{precision}f} {to_unit.upper()}')

        # Plot the graphical representation.
        plot_temperature_graph(value, from_unit)

    except ValueError:
        # Handle exceptions when non-numeric values are entered.
        print("Please enter a valid numerical temperature.")
    except Exception as e:
        # Handle any other exceptions that might occur during the execution.
        print(f'An error occurred: {e}')