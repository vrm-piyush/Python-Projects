# Multiple Input from User Program

![multiple input](../assets/images/readme_images/multiple_input.png)

## Project Overview

The Multiple Input from User Program is a Python-based utility that allows users to continuously input text until they decide to stop the program. The program provides additional functionalities, such as displaying the entered inputs, clearing the entered inputs, and keeping track of the count of inputs entered.

## Features

- **Continuous Input:**

  - Accepts user input until the user decides to stop by entering 'stop.'

- **Input Display:**

  - Allows users to display the list of entered inputs at any point by entering 'display.'

- **Input Clearing:**

  - Provides an option for users to clear the entered inputs by typing 'clear.'

- **Count of Inputs:**

  - Tracks and displays the count of inputs entered by the user.

- **Simple Command-Line Interface:**
  - Presents a simple and intuitive command-line interface for user interaction.

## How to Use

1. **Run the Program:**

   - Execute the program to start receiving user inputs.

2. **Enter Text:**

   - Input text when prompted. The program records regular text inputs.

3. **Display Entered Inputs:**

   - Type 'display' to see the list of entered inputs and their count.

4. **Clear Entered Inputs:**

   - Type 'clear' to reset and clear the entered inputs.

5. **Stop the Program:**
   - Enter 'stop' to end the program, and the entered inputs will be displayed.

## Example

```bash
cd MultipleInputProgram
python multiple_input_program.py
```

```python
    Menu-
    'Stop'    - end
    'Display' - Display text
    'Clear'   - Reset

    Enter text: Hello
    Input 'Hello' recorded.

    Enter text: World
    Input 'World' recorded.

    Enter text: Display
    Input 'Display' recorded.

    Enter text: display
    Display Inputs:
    1. Hello
    2. World
    3. Display
    4. display

    Enter text: Clear
    Input 'Clear' recorded.

    Enter text: clear
   	Entered inputs cleared.

    Enter text: Stop
   	Program ended.
```

## Features to be Added

- **Input Timestamps:**

  - Include timestamps for each entered input to track when they were recorded.

- **User Confirmation:**

  - Ask users for confirmation before clearing all entered inputs to avoid accidental data loss.

- **Interactive Menu:**

  - Enhance the menu system with interactive prompts for a more user-friendly experience.

- **Export Inputs:**

  - Allow users to export the entered inputs to a text file for later reference.

- **Input Editing:**

  - Enable users to edit previously entered inputs.

- **Custom User Prompts:**

  - Allow customization of user prompts for a more personalized user experience.

- **Input Filtering:**
  - Implement a filtering mechanism to exclude specific inputs from being displayed.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/Python-Projects/issues/new/choose) or refer to [contribution guidelines](../CONTRIBUTING.md) for more details.

---
