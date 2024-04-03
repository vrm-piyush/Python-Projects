"""
Digital Clock using GUI Program.

Input:
- No specific input required from the user.

Output:
- Displays a digital clock on a graphical user interface.

Features:
- Displays a digital clock in a graphical user interface.
- Allows the user to toggle between 12-hour and 24-hour time formats.
- Supports the option to display or hide the date.
- Provides a simple and intuitive user interface for viewing the time.
- Updates the clock display in real-time.

"""

# Import necessary modules from the tkinter library.
import tkinter as tk
from tkinter import font
import time

class DigitalClock:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Clock")
        self.root.configure(bg="#000000")  # Set the background color to black
        self.root.geometry("400x250")  # Set the initial window size

        # Font settings for digital clock display
        self.digital_font = font.Font(family='Boulder', size=40)

        # Variables
        self.show_date = False
        self.time_format_var = tk.StringVar()
        self.time_format_var.set("12")

        # Create digital clock frame
        self.digital_clock_frame = tk.Frame(self.root, bg="#000000")
        self.digital_clock_frame.pack(expand=True)

        # Create widgets in the digital clock frame
        self.label = tk.Label(self.digital_clock_frame, font=self.digital_font, bg="#000000", fg="#00FF00", bd=25)
        self.label.pack(expand=True)

        self.date_label = tk.Label(self.digital_clock_frame, font=('Boulder', 20), bg="#000000", fg="#00FF00")
        self.date_label.pack(expand=True)

        self.toggle_format_button = tk.Button(root, text="Toggle Format", command=self.toggle_time_format)
        self.toggle_format_button.pack(pady=5)

        self.toggle_date_button = tk.Button(root, text="Toggle Date", command=self.toggle_date_display)
        self.toggle_date_button.pack(pady=5)

        # Run the clock
        self.update_clock()

    def toggle_time_format(self):
        current_format = self.time_format_var.get()
        new_format = "12" if current_format == "24" else "24"
        self.time_format_var.set(new_format)


    def toggle_date_display(self):
        self.show_date = not self.show_date

    def update_clock(self):
        time_live = time.strftime(f"%{'I' if self.time_format_var.get() == '12' else 'H'}:%M:%S")
        self.label.config(text=time_live)

        if self.show_date:
            date = time.strftime("%Y-%m-%d")
            self.date_label.config(text=f"Date: {date}")
        else:
            self.date_label.config(text="")

        self.label.after(200, self.update_clock)

if __name__ == '__main__':
    root = tk.Tk()
    app = DigitalClock(root)
    root.mainloop()