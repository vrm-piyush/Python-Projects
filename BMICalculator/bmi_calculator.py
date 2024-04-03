"""
Body Mass Index (BMI) Calculator Program.

Input:
- User's weight in kilograms (Kg) or pounds (lb).
- User's height in meters (m) or inches (in).

Output:
- Calculated BMI value.
- Weight status based on BMI.

Features:
- Calculates BMI based on user's weight and height.
- Supports input in different units (kilograms/meters or pounds/inches).
- Displays BMI category and weight status.
- Allows the user to choose units for weight and height.
- Provides color-coded results for different weight statuses.
- Includes a BMI chart for reference.
- Handles invalid input and exceptions gracefully.

"""

from colorama import Fore, Style
from prettytable import PrettyTable

def convert_units(value, from_unit, to_unit):
    """
    Convert a value from one unit to another.

    Args:
    - value (float): The value to be converted.
    - from_unit (str): The original unit of the value.
    - to_unit (str): The desired unit for conversion.

    Returns:
    - float: The converted value.
    """
    unit_conversions = {
        ('kg', 'lb'): 2.20462,    # Conversion factor from kilograms to pounds
        ('lb', 'kg'): 0.453592,   # Conversion factor from pounds to kilograms
        ('m', 'in'): 39.3701,     # Conversion factor from meters to inches
        ('in', 'm'): 0.0254,      # Conversion factor from inches to meters
        ('m', 'm'): 1,            # Conversion factor from meters to meters
        ('kg', 'kg'): 1,          # Conversion factor from kilograms to kilograms
        ('kg', 'g'): 1000,        # Conversion factor from kilograms to grams
        ('g', 'kg'): 0.001,       # Conversion factor from grams to kilograms
        ('lb', 'g'): 453.592,     # Conversion factor from pounds to grams
        ('g', 'lb'): 0.00220462,  # Conversion factor from grams to pounds
        ('m', 'cm'): 100,         # Conversion factor from meters to centimeters
        ('cm', 'm'): 0.01,        # Conversion factor from centimeters to meters
        # Add more unit conversions as needed
    }

    conversion_key = (from_unit.lower(), to_unit.lower())

    if conversion_key in unit_conversions:
        conversion_factor = unit_conversions[conversion_key]
        return value * conversion_factor
    else:
        # Units not supported for conversion
        raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")

def get_unit_input(prompt, units):
    """
    Get valid unit input from the user.

    Args:
    - prompt (str): The prompt to display to the user.
    - units (list): List of valid units.

    Returns:
    - str: The selected unit.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in units:
            return user_input
        else:
            print(f"Invalid unit. Please choose from: {', '.join(units)}")

def get_user_data():
    """
    Get user input for weight and height, including unit selection.

    Returns:
    - tuple: Tuple containing weight, weight_unit, height, and height_unit.
    """
    weight_units = ['kg', 'lb', 'g']
    height_units = ['m', 'cm', 'in']

    while True:
        try:
            weight = float(input('Enter your weight: '))
            if weight <= 0:
                raise ValueError("Weight must be a positive value.")

            weight_unit = get_unit_input(f'Choose weight unit ({", ".join(weight_units)}): ', weight_units)

            height = float(input('Enter your height: '))
            if height <= 0:
                raise ValueError("Height must be a positive value.")

            height_unit = get_unit_input(f'Choose height unit ({", ".join(height_units)}): ', height_units)

            return weight, weight_unit, height, height_unit

        except ValueError as ve:
            print(f'Error: {ve}')

def display_bmi_chart():
    table = PrettyTable()
    table.field_names = ["BMI Category", "BMI Range"]

    bmi_categories = [
        ("Underweight", "BMI < 18.5"),
        ("Normal Weight", "18.5 <= BMI < 24.9"),
        ("Overweight", "25 <= BMI < 29.9"),
        ("Obesity", "BMI >= 30")
    ]

    for category, bmi_range in bmi_categories:
        table.add_row([category, bmi_range])

    print("\nBMI Chart:")
    print(table)


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculate the Body Mass Index (BMI) using the weight and height provided.
    
    Formula: BMI = weight (kg) / (height (m))^2
    
    Args:
    - weight (float): Weight of the user in kilograms.
    - height (float): Height of the user in meters.
    
    Returns:
    - float: Calculated BMI value.
    """
    return weight / (height ** 2)

def interpret_bmi(bmi: float) -> str:
    """
    Interpret the BMI value to determine the weight status of the user.
    
    Args:
    - bmi (float): Calculated BMI value.
    
    Returns:
    - str: Weight status category based on BMI with color-coding.
    """
    if bmi < 18.5:
        return f"{Fore.BLUE}Underweight{Style.RESET_ALL}"
    elif 18.5 <= bmi <= 24.9:
        return f"{Fore.GREEN}Normal Weight{Style.RESET_ALL}"
    elif 25 <= bmi <= 29.9:
        return f"{Fore.YELLOW}Overweight{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Obesity{Style.RESET_ALL}"


if __name__ == '__main__':
    try:
        weight, weight_unit, height, height_unit = get_user_data()

        # Convert weight and height to standard units (kg and meters)
        weight_kg = convert_units(weight, weight_unit, 'kg')
        height_m = convert_units(height, height_unit, 'm')

        # Calculate the BMI value using the provided weight and height.
        bmi = calculate_bmi(weight_kg, height_m)

        # Interpret the BMI value to determine the weight status.
        status = interpret_bmi(bmi)

        # Display the BMI chart
        display_bmi_chart()

        # Display the calculated BMI value and weight status to the user.
        print(f'Your BMI is {bmi:.3f}')
        print(f'You are categorized as {status}')

    except ValueError:
        # Handle exceptions when non-numeric values are entered.
        print('Please enter valid numerical values for Weight and Height!')