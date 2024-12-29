# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Weight Converter GUI Program.

Input:
- User interaction to input weight, choose units, and set decimal places.
- Keyboard shortcuts (Ctrl+C for conversion, Ctrl+L for clearing fields).

Output:
- Converted weight displayed with specified units and decimal places.
- Error messages for invalid input or negative weight.

Features:
- Allows users to input a weight, choose units for conversion, and set the desired decimal places.
- Provides a Convert button to perform the weight conversion.
- Supports keyboard shortcuts (Ctrl+C for conversion, Ctrl+L for clearing fields).
- Displays the converted weight with the specified units and decimal places.
- Handles errors for invalid input (non-numeric or negative weight values).
- Provides an About menu to display information about the application.

"""

from tkinter import (ttk, StringVar, Label, Entry, OptionMenu, Menu, Spinbox,
                    IntVar, Button, Text, END, messagebox, Tk)

class WeightConverterApp:
    def __init__(self, master):
        """
        Initialize the Weight Converter GUI.

        Args:
        - master: Tkinter root window.
        """
        self.master = master
        master.title('Weight Converter')

        # Set ttk theme
        self.style = ttk.Style()
        self.style.theme_use('vista')  # Choose a ttk theme (e.g., 'clam', 'alt', 'default', 'vista')

        # Unit options
        self.units = {
            "kilograms": "kg",
            "grams": "g",
            "milligrams": "mg",
            "pounds": "lb",
            "ounces": "oz",
            "stones": "st"
        }

        # Variables
        self.from_unit_var = StringVar(value="kilograms")
        self.to_unit_var = StringVar(value="grams")
        self.weight_value = StringVar()
        self.decimal_places = IntVar(value=2)

        # Menu Bar
        menubar = Menu(master)
        master.config(menu=menubar)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)
        
        # Shortcuts Menu
        shortcut_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Shortcuts", menu=shortcut_menu)
        
        # Dropdown menu for shortcuts
        shortcuts_menu = Menu(shortcut_menu, tearoff=0)
        shortcut_menu.add_cascade(label="Show Shortcuts", menu=shortcuts_menu)
        
        # Add individual shortcut items
        shortcuts_menu.add_command(label="Convert (Ctrl+C)", command=lambda: self.convert_weight())
        shortcuts_menu.add_command(label="Clear (Ctrl+L)", command=lambda: self.clear_fields)

        # Labels
        Label(master, text="Input the weight:\t\t").grid(row=1, column=0, columnspan=4)

        # Entry for weight value with validation
        self.weight_entry = Entry(master, textvariable=self.weight_value)
        self.weight_entry.grid(row=1, column=3, columnspan=4, padx=5, pady=10, sticky="w")

        # Dropdowns for unit selection
        OptionMenu(master, self.from_unit_var, *self.units.keys()).grid(row=3, column=0, padx=5, pady=10, sticky="w")
        OptionMenu(master, self.to_unit_var, *self.units.keys()).grid(row=3, column=1, padx=5, pady=10, sticky="w")

        # Decimal Places Setting
        Label(master, text="Decimal Places:").grid(row=3, column=2, padx=5, pady=10, sticky="w")
        Spinbox(master, from_=0, to=10, textvariable=self.decimal_places).grid(row=3, column=3, padx=5, pady=10, sticky="w")

        # Conversion Button
        Button(master, text="Convert", command=self.convert_weight).grid(row=3, column=4, padx=5, pady=10, sticky="w")

        # Result Text Widgets
        self.result_text = Text(master, height=5, width=35)
        self.result_text.grid(row=4, column=1, columnspan=6, padx=5, pady=5, sticky="w")

        # Clear Button
        Button(master, text="Clear", command=self.clear_fields).grid(row=3, column=5, padx=5, pady=10, sticky="w")

        # Keyboard Shortcuts
        master.bind('<Control-c>', lambda event: self.convert_weight())
        master.bind('<Control-l>', lambda event: self.clear_fields())

    def convert_weight(self):
        """
        Convert the weight based on user input.
        """
        try:
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            weight_value = float(self.weight_value.get())
            decimal_places = int(self.decimal_places.get())

            # Validation for non-negative weight values
            if weight_value < 0:
                raise ValueError("Weight must be non-negative.")

            conversion_factors = {
                "kilograms": {"grams": 1000, "milligrams": 1e6, "pounds": 2.20462, "ounces": 35.274, "stones": 0.157473},
                "grams": {"kilograms": 0.001, "milligrams": 1000, "pounds": 0.00220462, "ounces": 0.035274, "stones": 0.000157473},
                "milligrams": {"kilograms": 1e-6, "grams": 0.001, "pounds": 2.20462e-6, "ounces": 3.5274e-5, "stones": 1.57473e-7},
                "pounds": {"kilograms": 0.453592, "grams": 453.592, "milligrams": 453592, "ounces": 16, "stones": 0.0714286},
                "ounces": {"kilograms": 0.0283495, "grams": 28.3495, "milligrams": 28349.5, "pounds": 0.0625, "stones": 0.00446429},
                "stones": {"kilograms": 6.35029, "grams": 6350.29, "milligrams": 6.35029e6, "pounds": 14, "ounces": 224}
            }

            if from_unit not in conversion_factors or to_unit not in conversion_factors[from_unit]:
                raise ValueError("Invalid unit seletion.")

            # Perform the conversion
            if from_unit == to_unit:
                converted_weight = 1
            else:
                converted_weight = weight_value * conversion_factors[from_unit][to_unit]

            # Display the result with unit abbreviation and desired decimal places
            result_text = f"{converted_weight:.{decimal_places}f} {self.units[to_unit]}"
            self.result_text.delete("1.0", END)
            self.result_text.insert(END, result_text)

        except ValueError as e:
            # Handle the case where the input is not a valid number or non-negative
            self.result_text.delete("1.0", END)
            self.result_text.insert(END, f"Error: {e}")
        except Exception as e:
            # Handle other unexpected errors
            self.result_text.delete("1.0", END)
            self.result_text.insert(END, f"An unexpected error occurred: {e}")

    def clear_fields(self):
        """
        Clear all input and output fields.
        """
        self.weight_value.set("")
        self.from_unit_var.set("kilograms")
        self.to_unit_var.set("grams")
        self.decimal_places.set(2)
        self.result_text.delete("1.0", END)
    
    def show_about_info(self):
        """
        Display information about the application.
        """
        about_info = """Weight Converter App
        Version 1.0
        Developer: Piyush Verma
        \nA simple GUI application to convert weights between different units."""
        messagebox.showinfo("About", about_info)

if __name__ == '__main__':
    root = Tk()
    
    # Configure ttk theme styles
    style = ttk.Style(root)
    style.configure("TButton", padding=5)
    style.configure("TEntry", padding=5)

    # Set the window size
    root.geometry("555x200")

    app = WeightConverterApp(root)
    root.mainloop()