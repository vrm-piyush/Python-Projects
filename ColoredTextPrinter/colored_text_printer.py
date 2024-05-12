# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Colored Text Printer Program.

Input:
- Text to display in color.
- Choices for text color and background color.

Output:
- Displayed text in the chosen colors.

Features:
- Allows the user to input multiple lines of text with customized colors and styles.
- Provides a menu for choosing text color, background color, and text styles.
- Validates user input to ensure that the chosen colors and styles are valid.
- Prints the entered text with the specified colors and styles using the Colorama library.
- Resets the text color and styles after printing each line of text.
- Provides an option to save the colored text as an HTML file.
- Generates an HTML file with the colored text using the specified colors and styles.

"""

import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

def print_colored_text(lines):
    """
    Print multiple lines of text with specified text, background colors, and styles.
    
    Args:
    - lines (list of tuples): Each tuple contains (text, text_color, bg_color, styles).
    """

    for line in lines:
        text, text_color, bg_color, styles = line
        style_str = '+'.join(styles)
        colored_text = (
            getattr(Fore, text_color.upper()) +
            getattr(Back, bg_color.upper()) +
            getattr(Style, style_str.upper()) +
            text +
            Style.RESET_ALL  # Reset styles after printing
        )
        print(colored_text)

def generate_html(lines, filename='colored_text_output.html'):
    """
    Generate an HTML file with the colored text.
    
    Args:
    - lines (list of tuples): Each tuple contains (text, text_color, bg_color, styles).
    - filename (str): The name of the HTML file to be generated.
    """
    with open(filename, 'w') as html_file:
        html_file.write('<html>\n<head>\n<title>Colored Text</title>\n</head>\n<body>\n')
        
        for line in lines:
            text, text_color, bg_color, styles = line
            style_str = ' '.join(styles)
            html_line = (
                f'<p style="color:{text_color}; background-color:{bg_color}; font-weight:{style_str}">'
                f'{text}'
                '</p>\n'
            )
            html_file.write(html_line)
        
        html_file.write('</body>\n</html>\n')

if __name__ == '__main__':
    lines = []
    
    while True:
        user_input = input('Enter a line of text (or type "done" to finish): ')

        if user_input.lower() == 'done':
            break

        print('Choose text color:')
        text_color = input('Options: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE\n').upper()

        print('Choose background color:')
        bg_color = input('Options: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE\n').upper()

        print('Choose text styles (comma-separated, e.g., BRIGHT,UNDERLINE):')
        styles_input = input('Options: BRIGHT, DIM, NORMAL, RESET_ALL: ').upper()
        styles = [s.strip() for s in styles_input.split(',')]

        valid_colors = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']
        valid_styles = ['BRIGHT', 'DIM', 'NORMAL', 'RESET_ALL']

        if text_color not in valid_colors or bg_color not in valid_colors or any(style not in valid_styles for style in styles):
            print('Invalid color or style choice!')
        else:
            lines.append((user_input,text_color,bg_color,styles))
    if lines:
        print('\nPrinting Colored Text: ')
        print_colored_text(lines)

        save_as_html_option = input('Do you want to save this as HTML? (y/n): ').lower()
        if save_as_html_option == 'y':
            html_filename = input('Enter the HTML filename (e.g., colored_text_output.html): ')
            generate_html(lines, html_filename)
            print(f'Colored text saved as {html_filename}')