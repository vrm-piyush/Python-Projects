"""
Roman Numeral to Decimal and Decimal to Roman Numeral Converter GUI Program.

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
- Provides a graphical user interface (GUI) for user interaction.
- Handles unexpected errors gracefully and provides informative messages.
- Provides clear instructions and error messages to the user.
- Uses radio buttons for user to select conversion direction.

"""

import tkinter as tk
from tkinter import ttk
import re

class RomanDecimalConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roman Numeral Converter")

        self.direction_var = tk.StringVar()
        self.direction_var.set("R")

        # Dictionary mapping Roman numerals to their decimal equivalents.
        self.tallies = {
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

        self.create_widgets()

    def create_widgets(self):
        # Direction selection (Radio buttons)
        direction_label = tk.Label(self.root, text="Conversion Direction:")
        direction_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        radio_frame = ttk.Frame(self.root)
        radio_frame.grid(row=1, column=0, padx=10, pady=5)

        radio_roman = ttk.Radiobutton(radio_frame, text="Roman to Decimal", variable=self.direction_var, value="R")
        radio_decimal = ttk.Radiobutton(radio_frame, text="Decimal to Roman", variable=self.direction_var, value="D")

        radio_roman.grid(row=0, column=0, padx=5)
        radio_decimal.grid(row=0, column=1, padx=5)

        # Entry for user input
        input_label = tk.Label(self.root, text="Enter Roman numeral or Decimal value:")
        input_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.input_entry = tk.Entry(self.root, width=30)
        self.input_entry.grid(row=3, column=0, padx=10, pady=5)

        # Button to perform conversion
        convert_button = tk.Button(self.root, text="Convert", command=self.perform_conversion)
        convert_button.grid(row=4, column=0, pady=10)

        # Display result label
        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=5, column=0, pady=5)

    def is_valid_roman_numeral(self, roman_numeral: str) -> bool:
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

    def is_valid_decimal_value(self, decimal_value: int) -> bool:
        """
        Check if the entered decimal value is within a valid range.
        
        Args:
        - decimal_value (int): Decimal value to check.
        
        Returns:
        - bool: True if the decimal value is valid, False otherwise.
        """
        return -10000 <= decimal_value <= 10000

    def RomanNumeralToDecimal(self, romanNumeral: str) -> int:
        """
        Convert a Roman numeral to its decimal equivalent.
        
        Args:
        - romanNumeral (str): Roman numeral string to convert.
        
        Returns:
        - int: Decimal equivalent of the Roman numeral.
        """

        decimal_value = 0
        prev_value = 0
        
        # Iterate through the Roman numeral string from right to left.
        for numeral in romanNumeral[::-1]:
            value = self.tallies[numeral]
            if value < prev_value:
                decimal_value -= value
            else:
                decimal_value += value
            prev_value = value
        
        return decimal_value

    def DecimalToRomanNumeral(self, decimal_value: int) -> str:
        """
        Convert a decimal value to its Roman numeral equivalent.
        
        Args:
        - decimal_value (int): Decimal value to convert.
        
        Returns:
        - str: Roman numeral equivalent of the decimal value.
        """

        if decimal_value < 0:
            # Handle negative decimal values
            return '-' + self.DecimalToRomanNumeral(-decimal_value)

        roman_numerals = ''
        
        for numeral, value in sorted(self.tallies.items(), reverse=True, key=lambda x: x[1]):
            while decimal_value >= value:
                roman_numerals += numeral
                decimal_value -= value
        
        # Replace any invalid patterns in the Roman numeral representation.
        roman_numerals = roman_numerals.replace('IIII', 'IV').replace('VIV', 'IX').replace('XXXX', 'XL').replace('LXL', 'XC').replace('CCCC', 'CD').replace('DCD', 'CM')
        
        return roman_numerals

    def perform_conversion(self):
        try:
            user_input = self.input_entry.get().strip()

            if self.direction_var.get() == "R":
                if self.is_valid_roman_numeral(user_input):
                    decimal_value = self.RomanNumeralToDecimal(user_input.upper())
                    self.result_label.config(text=f'The decimal equivalent is {decimal_value}')
                else:
                    self.result_label.config(text='Error: Invalid Roman numeral. Please enter a valid Roman numeral.')

            elif self.direction_var.get() == "D":
                decimal_value = int(user_input)
                if self.is_valid_decimal_value(decimal_value):
                    roman_numeral = self.DecimalToRomanNumeral(decimal_value)
                    self.result_label.config(text=f'The Roman numeral equivalent is {roman_numeral}')
                else:
                    self.result_label.config(text='Error: Invalid decimal value. Please enter a value between 1 and 3999.')

        except ValueError:
            self.result_label.config(text='Error: Please enter a valid numerical value.')
        except Exception as e:
            self.result_label.config(text=f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    root = tk.Tk()
    app = RomanDecimalConverterApp(root)
    root.mainloop()
