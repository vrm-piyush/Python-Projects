"""
Multiple Input from User Program.

Input:
- 'stop' to end the program.
- 'display' to show the entered inputs.
- 'clear' to reset and clear the entered inputs.
- Any other input is considered as regular text input.

Output:
- Displays each regular text input.
- Shows the count of inputs entered.

Features:
- Continuously receives inputs from the user until the input is 'stop'.
- Tracks the count of inputs entered.
- Allows the user to display the entered inputs.
- Provides an option to clear the entered inputs.
- Handles invalid input and exceptions gracefully.
- Provides a simple and intuitive command-line interface for users to interact with the program.

"""

def display_user_inputs(inputs: list):
    """
    Display the entered inputs from the user.

    Args:
    - inputs (list): List of user inputs to display.
    """
    if inputs:
        print("\n\tEntered Inputs:")
        for i, user_input in enumerate(inputs, 1):
            print(f"\t{i}. {user_input}")
    else:
        print("\tNo inputs entered yet.")

if __name__ == '__main__':
    user_inputs = []

    while True:
        # Receive input from the user.
        reply = input(
            "\n\tMenu-\n\
            'Stop'    - end\n\
            'Display' - Display text\n\
            'Clear'   - Reset\t\t\
            \n\n\tEnter text: "
        )

        # Check if the user wants to stop the program.
        if reply.lower() == 'stop':
            display_user_inputs(user_inputs)
            break

        # Check if the user wants to display the entered inputs.
        elif reply.lower() == 'display':
            display_user_inputs(user_inputs)

        # Check if the user wants to clear the entered inputs.
        elif reply.lower() == 'clear':
            user_inputs = []
            print("\t\tEntered inputs cleared.")
        # Regular text input.
        else:
            user_inputs.append(reply)
            print(f"\tInput '{reply}' recorded.")

    print("\nProgram ended.")
