# Temperature Converter Program

![temperature converter](image.png)

## Project Overview

The Temperature Converter Program is a Python-based utility that facilitates the conversion of temperature values between various units, including Fahrenheit (F), Celsius (C), Kelvin (K), Rankine (R), Delisle (DE), and Newton (N). The program not only converts temperatures but also provides a graphical representation of the temperature value on different scales, allowing users to visualize the conversion results.

## Features

- **Temperature Unit Conversion:**

  - Converts temperature values between Fahrenheit, Celsius, Kelvin, Rankine, Delisle, and Newton units.

- **Graphical Representation:**

  - Utilizes Matplotlib to create a graphical representation (chart or graph) of the temperature value on different scales.

- **Validation and Exception Handling:**

  - Validates temperature input against specified ranges for each unit, ensuring that entered values are within valid limits.
  - Handles exceptions gracefully, providing informative error messages for better user guidance.

- **Customizable Precision:**

  - Supports customizable precision for the converted temperature values, allowing users to specify the number of decimal places.

- **Interactive Command-Line Interface:**
  - Provides a simple and intuitive command-line interface for users to interact with the program seamlessly.

## How to Use

1. **Run the Program:**

   - Execute the program to start the Temperature Converter.

2. **Enter Temperature Details:**

   - Input the temperature value, the unit to convert from, the unit to convert to, and the desired precision when prompted.

3. **View Results:**

   - The program will display the converted temperature value with the specified precision.

4. **Graphical Representation:**
   - A graphical representation of the temperature value on different scales will be shown using Matplotlib.

## Example

```bash
cd TemperatureConverter
python temperature_converter.py
```

```python
Enter the temperature value: 32
Enter the unit of temperature to convert from (F, C, K, R, DE, N.): F
Enter the unit of temperature to convert to (F, C, K, R, DE, N.): C
Enter the precision (number of decimal places): 2

32.0 F is equal to 0.00 C
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/vrm-piyush/TemperatureConverter.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd TemperatureConverter
   ```

3. **Run the Program:**

   ```bash
   python temperature_converter.py
   ```

## Features to be Added

- **Interactive Unit Selection:**

  - Enhance user experience by implementing an interactive menu for selecting temperature units.

- **Temperature Scales Information:**

  - Provide informational details about different temperature scales for educational purposes.

- **Temperature Incremental Conversion:**

  - Enable the conversion of a series of temperatures at once and display the results.

- **Error Handling Improvement:**

  - Enhance error handling with more specific messages to guide users in case of input errors.

- **Unit Abbreviation Auto-Completion:**

  - Implement a feature that suggests and completes unit names based on partial abbreviations entered by the user.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/TemperatureConverter/issues) or submit a pull request.

---
