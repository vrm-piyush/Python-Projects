"""
Calculator GUI Program.

Input:
- User interaction with the Calculator GUI.

Output:
- Calculator screen with basic arithmetic operations.

Features:
- Implements a basic calculator with a graphical user interface using Kivy.
- Supports arithmetic operations such as addition, subtraction, multiplication, and division.
- Provides buttons for digits (0-9), decimal point, percentage, and common arithmetic operators.
- Includes special buttons for clearing the entire input, clearing the current input, and deleting the last character.
- Displays the current calculation on the screen.
- Shows a calculation history with results in a scrollable area.

"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class Calculator(App):
    def build(self):
        # Initialize calculator state
        self.history = []

        # Create the root layout as a vertical box
        root_layout = BoxLayout(orientation='vertical')

        # Create the output label for displaying current calculation
        self.output_label = Label(size_hint_y=0.75, font_size=50)

        # Create the history label for displaying calculation history
        self.history_label = Label(size_hint_y=0.25, font_size=20, halign='left', valign='top', text_size=(None, None))
        self.history_scroll = ScrollView(size_hint_y=0.25)

        # Define the symbols on the calculator buttons
        button_symbols = ('CE', 'C', 'DEL', '/',
                          '9', '8', '7', '*',
                          '4', '5', '6', '-',
                          '1', '2', '3', '+',
                          '%', '0', '.', '=')

        # Create the button grid
        button_grid = self.create_button_grid(button_symbols)

        # Add widgets to the root layout
        root_layout.add_widget(self.output_label)
        self.history_scroll.add_widget(self.history_label)
        root_layout.add_widget(self.history_scroll)
        root_layout.add_widget(button_grid)

        return root_layout

    def create_button_grid(self, button_symbols):
        # Create the button grid layout with 4 columns
        button_grid = GridLayout(cols=4, size_hint_y=2)

        # Populate the button grid with buttons using button_symbols
        for symbol in button_symbols:
            button = Button(text=symbol)
            button.bind(on_press=self.on_button_press) # type:ignore
            button_grid.add_widget(button)

        return button_grid

    def on_button_press(self, instance):
        # Handle button press events
        if instance.text == '=':
            self.evaluate_result()
        elif instance.text == 'CE':
            self.clear_all(instance)
        elif instance.text == 'C':
            self.clear_output(instance)
        elif instance.text == 'DEL':
            self.delete_last_char()
        else:
            self.update_output_label(instance.text)

    def evaluate_result(self):
        # Evaluate the current calculation and update labels
        try:
            result = eval(self.output_label.text)
            self.history.append(f'{self.output_label.text} = {result}')
            self.output_label.text = str(result)
            self.update_history_label()
        except ZeroDivisionError:
            self.output_label.text = 'Error: Division by zero'
        except SyntaxError:
            self.output_label.text = 'Python Syntax Error!'

    def update_output_label(self, text):
        # Update the output label with the pressed button's text
        self.output_label.text += text

    def update_history_label(self):
        # Update the history label with the calculation history
        self.history_label.text = '\n'.join(self.history)

    def clear_all(self, instance):
        # Clear all input and history
        self.output_label.text = ""
        self.history = []
        self.update_history_label()

    def clear_output(self, instance):
        # Clear the current input
        self.output_label.text = ""

    def delete_last_char(self):
        # Delete the last character from the current input
        if self.output_label.text != "":
            self.output_label.text = self.output_label.text[:-1]

if __name__ == '__main__':
    # Run the Calculator application
    Calculator().run()




'''
Scientific Calculator Functions: Include additional scientific calculator functions such as square root, exponentiation, trigonometric functions (sin, cos, tan), logarithms, etc.

Memory Functions: Add memory-related functions like Memory Recall (MR), Memory Store (MS), Memory Clear (MC), and Memory Add (M+).

History Navigation: Allow users to navigate through the calculation history and recall or edit previous calculations.

Themes and Styles: Implement different themes and styles for the calculator, allowing users to customize the appearance.

Keyboard Support: Enable keyboard input for the calculator to enhance usability.

Copy-Paste Support: Allow users to copy and paste values to and from the calculator.

Floating Point Precision Control: Add an option to control the number of decimal places displayed in the result.

Error Handling: Improve error handling and display meaningful messages for various types of errors.

Unit Conversion: Integrate unit conversion functionality for common units (length, weight, temperature, etc.).

Expression History: Keep track of the entire expression entered by the user, not just the results.

Settings Panel: Include a settings panel where users can configure calculator preferences.

Resizable Fonts: Allow users to resize the font for better visibility.

Accessibility Features: Implement accessibility features such as voice output for the visually impaired.

Advanced Layouts: Explore different layouts, like a scientific calculator layout or a more compact layout.

Help/About Section: Provide a help or about section to guide users on how to use the calculator and display version information.
'''