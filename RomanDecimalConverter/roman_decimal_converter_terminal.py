"""
Roman Numeral to Decimal and Decimal to Roman Numeral Converter Program.

Input:
- Conversion direction (R for Roman to Decimal, D for Decimal to Roman).
- Input in Roman or Decimal numeral.

Output:
- Displays converted number.

Features:
- Validates the input Roman numeral for correctness.
- Validates the input decimal value for a valid range.
- Corrects invalid Roman numeral patterns during conversion.
- Handles negative decimal values.
- Provides a more user-friendly interface with clear instructions.
- Handles unexpected errors gracefully and provides informative messages.
- Supports conversion in both directions (Roman to Decimal and Decimal to Roman).

"""

import re

# Dictionary mapping Roman numerals to their decimal equivalents.
tallies = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
    'V̅': 5000,    # Overline (vinculum) represents multiplication by 1000
    'X̅': 10000,
    # Add more symbols as needed
}

def is_valid_roman_numeral(roman_numeral: str) -> bool:
    """
    Check if the entered Roman numeral is valid.
    
    Args:
    - roman_numeral (str): Roman numeral string to check.
    
    Returns:
    - bool: True if the Roman numeral is valid, False otherwise.
    """
    # Regular expression pattern to validate Roman numerals
    roman_pattern = r'^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}|V̅|X̅)$'
    return re.match(roman_pattern, roman_numeral.upper()) is not None

def is_valid_decimal_value(decimal_value: int) -> bool:
    """
    Check if the entered decimal value is within a valid range.
    
    Args:
    - decimal_value (int): Decimal value to check.
    
    Returns:
    - bool: True if the decimal value is valid, False otherwise.
    """
    return -10000 <= decimal_value <= 10000

def RomanNumeralToDecimal(roman_numeral: str) -> int:
    """
    Convert a Roman numeral to its decimal equivalent.
    
    Args:
    - roman_numeral (str): Roman numeral string to convert.
    
    Returns:
    - int: Decimal equivalent of the Roman numeral.
    """

    decimal_value = 0
    prev_value = 0
    
    # Iterate through the Roman numeral string from right to left.
    for numeral in roman_numeral[::-1]:
        value = tallies[numeral]
        if value < prev_value:
            decimal_value -= value
        else:
            decimal_value += value
        prev_value = value
    
    return decimal_value

def DecimalToRomanNumeral(decimal_value: int) -> str:
    """
    Convert a decimal value to its Roman numeral equivalent.
    
    Args:
    - decimal_value (int): Decimal value to convert.
    
    Returns:
    - str: Roman numeral equivalent of the decimal value.
    """

    if decimal_value < 0:
        # Handle negative decimal values
        return '-' + DecimalToRomanNumeral(-decimal_value)

    roman_numerals = ''
    
    for numeral, value in sorted(tallies.items(), reverse=True, key=lambda x: x[1]):
        while decimal_value >= value:
            roman_numerals += numeral
            decimal_value -= value
    
    # Replace any invalid patterns in the Roman numeral representation.
    roman_numerals = roman_numerals.replace('IIII', 'IV').replace('VIV', 'IX').replace('XXXX', 'XL').replace('LXL', 'XC').replace('CCCC', 'CD').replace('DCD', 'CM')
    
    return roman_numerals

if __name__ == '__main__':
    try:
        # Prompt the user to select the conversion direction.
        direction = input("Convert from Roman to Decimal (R) or Decimal to Roman (D)? ").upper()
        
        if direction == 'R':
            # Convert Roman numeral to decimal.
            roman_numeral = input('Enter the Roman numeral: ').upper()
            
            if is_valid_roman_numeral(roman_numeral):
                decimal_value = RomanNumeralToDecimal(roman_numeral)
                print(f'The decimal equivalent of {roman_numeral} is {decimal_value}')
            else:
                print('Error: Invalid Roman numeral. Please enter a valid Roman numeral.')
        elif direction == 'D':
            # Convert decimal to Roman numeral.
            decimal_value = int(input('Enter the decimal value: '))
            
            if is_valid_decimal_value(decimal_value):
                roman_numeral = DecimalToRomanNumeral(decimal_value)
                print(f'The Roman numeral equivalent of {decimal_value} is {roman_numeral}')
            else:
                print('Error: Invalid decimal value. Please enter a value between 1 and 3999.')
        else:
            print("Invalid choice. Please enter 'R' or 'D'.")
    
    except ValueError:
        print("Error: Please enter a valid numerical value.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')