"""
Dice Roll Simulation Program.

Input:
- Integer number of times to roll the dice.
- 'yes' or 'y' to roll the dice again, 'no' or 'n' to stop rolling.

Features:
- Multiplayer mode: Allows multiple players to roll different sets of dice with statistics, histogram, and probability calculation.
- Animated dice roll: Provides an animated histogram of dice rolls for a specified number of frames.
- Simulates rolling a dice with a specific number of sides.
- Handles input validation for user choices.
- Displays statistics about the rolled values (total sum, average, minimum, maximum).
- Displays a histogram of the rolled values.
- Displays the history of rolled values.
- Calculates and displays the probability of each possible outcome.

"""

import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def roll_dice(num_rolls, num_sides):
    """
    Simulate rolling a dice with a specific number of sides.

    Args:
    - num_rolls (int): Number of times to roll the dice.
    - num_sides (int): Number of sides on the dice.

    Returns:
    - list: List of rolled values.
    """
    return [random.randint(1, num_sides) for _ in range(num_rolls)]

def roll_dice_notation(dice_notation):
    """Roll dice based on the provided dice notation."""
    num_rolls, num_sides = map(int, dice_notation.split('d'))
    return roll_dice(num_rolls, num_sides)

def display_statistics(rolled_values, player_name):
    """
    Display statistics about the rolled values.

    Args:
    - rolled_values (list): List of rolled values.
    - player_name (str): Player's name.
    """
    total_sum = sum(rolled_values)
    average = total_sum / len(rolled_values)
    minimum_value = min(rolled_values)
    maximum_value = max(rolled_values)

    print(f"\nStatistics for {player_name}:")
    print(f"Total Sum: {total_sum}")
    print(f"Average: {average:.2f}")
    print(f"Minimum Value: {minimum_value}")
    print(f"Maximum Value: {maximum_value}")

def display_histogram(all_rolls, num_sides):
    """
    Display a histogram of the rolled values.

    Args:
    - rolled_values (list): List of rolled values.
    - num_sides (int): Number of sides on the dice.
    """
    plt.figure(figsize=(10, 6))

    for player, rolls in all_rolls.items():
        plt.hist(rolls, bins=range(1, num_sides + 2), alpha=0.5, label=player, align='left', rwidth=0.8)

    plt.xlabel('Dice Value')
    plt.ylabel('Frequency')
    plt.title('Dice Roll Histogram - Multiplayer Mode')
    plt.xticks(list(range(1, num_sides + 1)))  # Convert range to list
    plt.legend()
    plt.show()

def display_history(rolled_values):
    """
    Display the history of rolled values.

    Args:
    - rolled_values (list): List of rolled values.
    """
    print("\nRoll History:")
    print(rolled_values)

def calculate_probability(rolled_values, num_sides):
    """
    Calculate and display the probability of each possible outcome.

    Args:
    - rolled_values (list): List of rolled values.
    - num_sides (int): Number of sides on the dice.
    """
    probabilities = {i: rolled_values.count(i) / len(rolled_values) for i in range(1, num_sides + 1)}
    
    print("\nProbability of Each Outcome:")
    for value, probability in probabilities.items():
        print(f"Value {value}: {probability:.2%}")

def animated_dice_roll(num_rolls, num_sides):
    """
    Display an animated histogram of dice rolls.

    Args:
    - num_rolls (int): Number of times to roll the dice.
    - num_sides (int): Number of sides on the dice.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0.5, num_sides + 0.5)
    ax.set_ylim(0, num_rolls + 1)

    def update(frame):
        plt.cla()
        rolls = roll_dice(num_rolls, num_sides)
        ax.hist(rolls, bins=list(range(1, num_sides + 2)), align='left', rwidth=0.8)
        ax.set_title(f'Dice Rolls - {num_rolls}d{num_sides}')
        ax.set_xlabel('Dice Value')
        ax.set_ylabel('Frequency')

    ani = animation.FuncAnimation(fig, update, frames=10, interval=500, repeat=False)
    plt.show()

def multiplayer_mode():
    """
    Enable multiplayer mode for rolling multiple sets of dice.
    """
    all_rolls = {}
    rolled_history = []

    while True:
        try:
            num_players = int(input("\nEnter the number of players: "))
            num_sides = int(input("Enter the number of sides on the dice: "))
            num_rolls = int(input("Enter the number of times to roll the dice per player: "))
            
            if num_players <= 0 or num_sides <= 1 or num_rolls <= 0:
                raise ValueError("Invalid input. Please enter positive values.")
            
            for i in range(1, num_players + 1):
                player_name = f"Player {i}"
                dice_notation = input(f"\nEnter dice notation for {player_name} (e.g., 2d6): ")
                
                if 'd' in dice_notation:
                    rolls = roll_dice_notation(dice_notation)
                    rolled_history.extend(rolls)
                else:
                    rolls = roll_dice(num_rolls, num_sides)
                    rolled_history.extend(rolls)
                
                all_rolls[player_name] = rolls
                
                print(f"\n{player_name}'s rolls: {rolls}")
                display_statistics(rolls, player_name)
                calculate_probability(rolls, num_sides)
            
            display_histogram(all_rolls, num_sides)
            display_history(rolled_history)

            animate_choice = input("\nDo you want to animate the dice rolls for this round? (yes/y or no/n): ").lower()
            if animate_choice in ['yes', 'y']:
                animated_dice_roll(num_rolls, num_sides)

            another_round = input("\nDo you want to play another round of the game? (yes/y or no/n): ").lower()
            if another_round not in ['yes', 'y']:
                break
        except ValueError as e:
            print(f"Error: {e}. Please enter valid inputs.")
            
if __name__ == '__main__':
    multiplayer_mode()