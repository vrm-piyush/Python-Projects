# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Calendar App with GUI in Python.

Input:
- Year, month, and date picker.

Output:
- Calendar view with year, month, and week modes.

Features:
- Year, month, and week view modes.
- Navigation buttons to switch between views and years.
- Date picker for selecting a specific date.
- Theme customization with color selection.
- Highlighting of holidays.
- Option to save the calendar as an image.
- Print functionality for the calendar.

"""

import calendar
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, Label, Button, Entry, Frame, StringVar, font, ttk, colorchooser

class CalendarApp:
    def __init__(self, root):
        """
        Initialize the CalendarApp.

        Parameters:
        - root: Tkinter root window object.
        """
        self.root = root
        self.root.config(background='white')
        self.root.title("Calendar App")
        self.root.geometry("1000x750")  # Increased window size
        self.root.resizable(True, True)  # Added resizable option

        self.year_var = StringVar()
        self.month_var = StringVar()
        self.day_var = StringVar()

        self.view_mode = StringVar()
        self.view_mode.set('year')

        # Default theme
        self.current_theme = {
            'bg_color': 'white',
            'text_color': 'black',
            'button_bg1': 'lightblue',
            'button_bg2': 'lightgreen',
            'button_bg3': 'orange',
            'button_fg': 'black',
            'calendar_bg': 'lightgrey',
            'highlight_bg': 'yellow',
            'error_fg': 'red',
        }

        self.holidays = {
            (1,1): "New Year's Day",
            (8,15): "Independence Day",
            (12,25): "Christmas Day",
        }

        self.create_widgets()

    def create_widgets(self):
        self.header_frame = Frame(self.root, bg=self.current_theme['bg_color'])
        self.header_frame.pack(pady=20)  # Added pady for spacing

        self.cal_label = Label(self.header_frame, text="Calendar", fg=self.current_theme['text_color'], bg=self.current_theme['bg_color'], font=("algerian", 28), justify='center', anchor='center')
        self.cal_label.grid(row=0, column=1, pady=10)  # Centered title

        self.prev_year_button = Button(self.header_frame, text='<<', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg1'], command=self.prev_year)
        self.prev_year_button.grid(row=1, column=0, padx=10, pady=10)

        # Date picker
        self.date_picker_frame = Frame(self.header_frame, bg=self.current_theme['bg_color'])
        self.date_picker_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.day_dropdown = ttk.Combobox(self.date_picker_frame, textvariable=self.day_var, values=list(map(str, range(1,32))))
        self.month_dropdown = ttk.Combobox(self.date_picker_frame, textvariable=self.month_var, values=list(map(str, range(1,13))))
        self.year_entry = Entry(self.date_picker_frame, textvariable=self.year_var, font=("times", 12))

        self.day_dropdown.grid(row=0, column=0, padx=5)
        self.month_dropdown.grid(row=0, column=1, padx=5)
        self.year_entry.grid(row=0, column=2, padx=5)

        self.day_var.set(str(datetime.now().day))
        self.month_var.set(str(datetime.now().month))
        self.year_var.set(str(datetime.now().year))

        self.next_year_button = Button(self.header_frame, text='>>', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg1'], command=self.next_year)
        self.next_year_button.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        self.show_button = Button(self.header_frame, text='Show Calendar', fg=self.current_theme['text_color'], bg=self.current_theme['highlight_bg'], command=self.show_calendar)
        self.show_button.grid(row=1, column=3, pady=10, sticky='w')

        self.theme_button = Button(self.header_frame, text='Change Theme', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg3'], command=self.change_theme)
        self.theme_button.grid(row=1, column=4, padx=15, pady=10, sticky='e')

        self.exit_button = Button(self.header_frame, text='Exit', fg=self.current_theme['text_color'], bg=self.current_theme['error_fg'], command=self.root.destroy)
        self.exit_button.grid(row=1, column=5, padx=10, pady=10, sticky='e')

        self.year_button = Button(self.header_frame, text='Year View', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg2'], command=self.switch_to_year_view)
        self.year_button.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        self.week_view_button = Button(self.header_frame, text='Week View', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg2'], command=self.switch_to_week_view)
        self.week_view_button.grid(row=2, column=3, padx=10, pady=10, sticky='w')

        self.month_view_button = Button(self.header_frame, text='Month View', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg2'], command=self.switch_to_month_view)
        self.month_view_button.grid(row=2, column=4, padx=25, pady=10, sticky='w')

        self.calendar_frame = Frame(self.root, bg=self.current_theme['calendar_bg'])  # Set calendar area to grey
        self.calendar_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.show_calendar()

        self.header_frame.grid_columnconfigure(1, weight=1)  # Centered title
        self.header_frame.grid_columnconfigure(3, weight=1)  # Added weight to show button
        self.header_frame.grid_columnconfigure(4, weight=1)  # Added weight to theme button
        self.header_frame.grid_columnconfigure(5, weight=1)  # Added weight to exit button
        self.header_frame.grid_rowconfigure(1, weight=1)  # Added weight to date picker frame
        self.header_frame.grid_rowconfigure(2, weight=1)  # Added weight to buttons

        for i in range(3):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
            self.calendar_frame.grid_columnconfigure(i, weight=1)

        self.footer_frame = Frame(self.root, bg=self.current_theme['bg_color'])
        self.footer_frame.pack(side='bottom', fill='x')

        self.save_image_button = Button(self.footer_frame, text='Save Image', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg2'], command=self.save_as_image)
        self.save_image_button.grid(row=0, column=3, padx=30, pady=10, sticky='e')  # Keep the 'sticky' parameter to 'e' for right alignment

        self.print_button = Button(self.footer_frame, text='Print', fg=self.current_theme['text_color'], bg=self.current_theme['button_bg2'], command=self.print_calendar)
        self.print_button.grid(row=0, column=2, pady=10, sticky='e')  # Keep the 'sticky' parameter to 'e' for right alignment

        self.footer_frame.grid_columnconfigure(2, weight=2)  # Added weight to center the buttons



    def show_calendar(self):
        """
        Show the calendar based on the selected view mode (year, month, or week).
        """
        self.calendar_frame.destroy()
        self.calendar_frame = Frame(self.root, bg=self.current_theme['calendar_bg'])
        self.calendar_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())

            view_mode = self.view_mode.get()

            if view_mode == 'year':
                self.show_year(year)
            elif view_mode == 'month':
                self.show_month(year, month)
            elif view_mode == 'week':
                self.show_week(year, month)

        except ValueError:
            self.show_error("Invalid year input. Please enter a valid year.")

    def show_error(self, message):
        """
        Show an error message in the calendar frame.

        Parameters:
        - message: str, error message to display.
        """

        error_label = Label(self.calendar_frame, text=message, fg=self.current_theme['error_fg'], bg=self.current_theme['calendar_bg'], font=("times", 16, "bold"), justify='center', anchor='center')
        error_label.grid(row=0, column=0, padx=20, pady=10)

    def show_year(self, year):
        for i in range(1, 13):
            month_content = calendar.monthcalendar(year, i)
            month_name = calendar.month_name[i]
            gui_content = f'{month_name}\nMon Tue Wed Thu Fri Sat Sun\n'
            
            for week in month_content:
                for day in week:
                    if day == 0:
                        gui_content += '    '
                    else:
                        gui_content += f'{day:2}  '
                gui_content += '\n'

            row_pos = (i-1) // 4
            col_pos = (i-1) % 4

            cal_month = Label(self.calendar_frame, text=gui_content, font=font.Font(family="Consolas", size=10, weight="bold"), bg=self.current_theme['calendar_bg'], fg=self.current_theme['text_color'], justify='center', anchor='center')
            cal_month.grid(row=row_pos, column=col_pos, padx=20, pady=10)

            self.calendar_frame.grid_rowconfigure(row_pos, weight=1)
            self.calendar_frame.grid_columnconfigure(col_pos, weight=1)

    def show_month(self, year, month):
        month_content = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        gui_content = f'{month_name} {year}\n\nMon Tue Wed Thu Fri Sat Sun\n'

        holidays_info = {}
            
        for week in month_content:
            for day in week:
                if day == 0:
                    gui_content += '    '
                else:
                    day_str = f'{day:2}'
                    holiday_key = (month, day)

                    if holiday_key in self.holidays:
                        day_str = f'{day_str}'
                        holidays_info[holiday_key] = self.holidays[holiday_key]

                    gui_content += f'{day_str:2}  '
            gui_content += '\n'

        cal_month = Label(self.calendar_frame, text=gui_content, font=font.Font(family="Consolas", size=25, weight="bold"), bg=self.current_theme['calendar_bg'], fg=self.current_theme['text_color'], justify='center', anchor='center')
        cal_month.grid(row=0, column=0, padx=20, pady=10)

        row_offset = len(month_content) + 1
        for (month, day), event in holidays_info.items():
            holiday_label = Label(self.calendar_frame, text=f"{month}/{day}: {event}", font=font.Font(family="Consolas", size=12, weight="bold"), bg=self.current_theme['calendar_bg'], fg='red', justify='center', anchor='center')
            holiday_label.grid(row=row_offset, column=0, padx=20, pady=10, sticky='w')
            row_offset += 1

        self.calendar_frame.grid_rowconfigure(0, weight=1)
        self.calendar_frame.grid_columnconfigure(0, weight=1)

    def show_week(self, year, month):
        start_date = datetime(year, month, int(self.day_var.get()))
        end_date = start_date + timedelta(days=6)

        gui_content = f'Week View\n\n{start_date.strftime("%B %d, %Y")} - {end_date.strftime("%B %d, %Y")}\n\n'

        for i in range(7):
            current_day = start_date + timedelta(days=i)
            gui_content += f'{current_day.strftime("%a %d %b")}'
            if i < 6:
                gui_content += '    '

        cal_week = Label(self.calendar_frame, text=gui_content, font=font.Font(family="Consolas", size=14, weight="bold"), bg=self.current_theme['calendar_bg'], fg=self.current_theme['text_color'], justify='center', anchor='center')
        cal_week.grid(row=0, column=0, padx=10, pady=10)

        self.calendar_frame.grid_rowconfigure(0, weight=1)
        self.calendar_frame.grid_columnconfigure(0, weight=1)

    def prev_year(self):
        current_year = int(self.year_var.get())
        self.year_var.set(str(current_year - 1))
        self.show_calendar()

    def next_year(self):
        current_year = int(self.year_var.get())
        self.year_var.set(str(current_year + 1))
        self.show_calendar()

    def switch_to_year_view(self):
        self.view_mode.set('year')
        self.show_calendar()

    def switch_to_week_view(self):
        self.view_mode.set('week')
        self.show_calendar()

    def switch_to_month_view(self):
        self.view_mode.set('month')
        self.show_calendar()

    def change_theme(self):
         # Ask for a color for each element
        bg_color = colorchooser.askcolor(title="Choose Background Color")[1]
        button_bg1 = colorchooser.askcolor(title="Choose Button Background Color 1")[1]
        button_bg2 = colorchooser.askcolor(title="Choose Button Background Color 2")[1]
        text_color = colorchooser.askcolor(title="Choose Text Color")[1]
        highlight_bg = colorchooser.askcolor(title="Choose Highlight Background Color")[1]
        error_fg = colorchooser.askcolor(title="Choose Error Text Color")[1]

        if bg_color:
            self.current_theme['bg_color'] = bg_color
            self.root.config(background=bg_color)
            self.header_frame.config(bg=bg_color)
            self.date_picker_frame.config(bg=bg_color)
            self.calendar_frame.config(bg=bg_color)

        if button_bg1:
            self.current_theme['button_bg1'] = button_bg1

        if button_bg2:
            self.current_theme['button_bg2'] = button_bg2

        if text_color:
            self.current_theme['text_color'] = text_color

        if highlight_bg:
            self.current_theme['highlight_bg'] = highlight_bg

        if error_fg:
            self.current_theme['error_fg'] = error_fg

        self.update_elements_color()
        self.show_calendar()

    def update_elements_color(self):
        # Update colors of individual elements
        self.prev_year_button.config(bg=self.current_theme['button_bg1'])
        self.next_year_button.config(bg=self.current_theme['button_bg1'])
        self.show_button.config(bg=self.current_theme['highlight_bg'])
        self.exit_button.config(bg=self.current_theme['error_fg'], fg=self.current_theme['text_color'])
        self.year_button.config(bg=self.current_theme['button_bg2'])
        self.week_view_button.config(bg=self.current_theme['button_bg2'])
        self.month_view_button.config(bg=self.current_theme['button_bg2'])
        self.cal_label.config(fg=self.current_theme['text_color'], bg=self.current_theme['bg_color'])
    
    def get_printable_content(self):
        printable_content = f"Printed Calendar - {calendar.month_name[int(self.month_var.get())]}, {self.year_var.get()}\n\n"

        view_mode = self.view_mode.get()

        if view_mode == 'year':
            printable_content += self.get_year_content(int(self.year_var.get()))
        elif view_mode == 'month':
            printable_content += self.get_month_content(int(self.year_var.get()), int(self.month_var.get()))
        elif view_mode == 'week':
            printable_content += self.get_week_content(int(self.year_var.get()), int(self.month_var.get()))

        return printable_content

    def get_month_content(self, year, month):
        month_content = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        printable_content = f'{month_name} {year}\n\nMon Tue Wed Thu Fri Sat Sun\n'

        holidays_info = {}
            
        for week in month_content:
            for day in week:
                if day == 0:
                    printable_content += '    '
                else:
                    day_str = f'{day:2}'
                    holiday_key = (month, day)

                    if holiday_key in self.holidays:
                        day_str = f'{day_str}'
                        holidays_info[holiday_key] = self.holidays[holiday_key]

                    printable_content += f'{day_str:2}  '
            printable_content += '\n'

        printable_content += '\n'

        for (month, day), event in holidays_info.items():
            printable_content += f"{month}/{day}: {event}\n"

        return printable_content

    def get_year_content(self, year):
        printable_content = ''
        for i in range(1, 13):
            month_content = calendar.monthcalendar(year, i)
            month_name = calendar.month_name[i]
            printable_content += f'{month_name}\nMon Tue Wed Thu Fri Sat Sun\n'
            
            for week in month_content:
                for day in week:
                    if day == 0:
                        printable_content += '    '
                    else:
                        printable_content += f'{day:2}  '
                printable_content += '\n'
            printable_content += '\n'

        return printable_content

    def get_week_content(self, year, month):
        start_date = datetime(year, month, int(self.day_var.get()))
        end_date = start_date + timedelta(days=6)

        printable_content = f'Week View\n\n{start_date.strftime("%B %d, %Y")} - {end_date.strftime("%B %d, %Y")}\n\n'

        for i in range(7):
            current_day = start_date + timedelta(days=i)
            printable_content += f'{current_day.strftime("%a %d %b")}'
            if i < 6:
                printable_content += '    '

        return printable_content
    
    def print_calendar(self):
        printable_content = self.get_printable_content()
        print(printable_content)

    def save_as_image(self):
        printable_content = self.get_printable_content()

        img = Image.new('RGB', (800, 750), color = (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        draw.text((10, 10), printable_content, fill=self.current_theme['text_color'], font=font)        

        img.save('calendar.png')
        print("Calendar saved as image")

if __name__ == '__main__':
    root = Tk()
    app = CalendarApp(root)
    root.mainloop()