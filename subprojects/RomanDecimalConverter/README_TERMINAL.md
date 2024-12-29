# Roman Numeral to Decimal and Decimal to Roman Numeral Converter (Terminal)

![RomanDecimal](../../assets/images/readme_images/roman_decimal_terminal.png)

## Project Overview

The Roman Numeral to Decimal and Decimal to Roman Numeral Converter Program is a Python-based utility that performs conversions between Roman numerals and decimal values through terminal interaction. The program includes features such as input validation, correction of invalid Roman numeral patterns, handling negative decimal values, and providing clear instructions to the user.

## Features

- **Conversion Direction:**

  - Allows users to choose the conversion direction: Roman to Decimal or Decimal to Roman.

- **Input Validation:**

  - Validates the input Roman numeral for correctness using regular expressions.
  - Validates the input decimal value for a valid range.

- **Error Handling:**

  - Handles unexpected errors gracefully and provides informative messages to guide the user.

- **Correction of Invalid Patterns:**

  - Corrects invalid Roman numeral patterns during conversion for accurate results.

- **Negative Decimal Values:**

  - Handles negative decimal values and provides accurate Roman numeral representation.

- **User-Friendly Interface:**
  - Presents a simple and intuitive interface with clear instructions for the user.

## How to Use

1. **Run the Program:**

   - Execute the program to start the terminal interaction.

2. **Select Conversion Direction:**

   - Enter 'R' for Roman to Decimal conversion or 'D' for Decimal to Roman conversion.

3. **Enter Input:**

   - Follow the prompts to enter the Roman numeral or decimal value.

4. **View Result:**

   - The result of the conversion is displayed on the terminal.

5. **Handle Errors:**

   - If an error occurs, an informative error message will be displayed.

6. **Close the Program:**
   - The program will end after completing the conversion or handling an error.

## Example

```bash
cd RomanDecimalConverter
python roman_decimal_converter_terminal.py
```

```bash
Convert from Roman to Decimal (R) or Decimal to Roman (D)? R
Enter the Roman numeral: XIV
The decimal equivalent of XIV is 14
```

## Features to be Added

- **Unit Tests:**

  - Implement unit tests to ensure the correctness of the conversion functions.

- **Conversion History:**

  - Maintain a history of conversions, allowing users to review their previous inputs and results.

- **Support for Lowercase Roman Numerals:**

  - Allow the user to input lowercase Roman numerals and handle the conversion appropriately.

- **Decimal Value Auto-Completion:**

  - Implement a feature that allows users to enter partial decimal values, and the program suggests and completes the full value.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/Python-Projects/issues/new/choose) or refer to [contribution guidelines](../../CONTRIBUTING.md) for more details.

---
