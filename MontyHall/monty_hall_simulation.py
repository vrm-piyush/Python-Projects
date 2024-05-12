# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Monty Hall Game Simulation Program.

Input:
- No input required from user.

Output:
- Winning percentage with and without changing.

Features:
- Simulates the Monty Hall game with a specified number of trials.
- Calculates and displays the winning percentage both with and without changing the initial choice.

"""

import random

def game(winning_door: int, selected_door: int, change: bool = False) -> bool:
    """
    Simulates the Monty Hall game and returns a boolean indicating if the player wins.
    
    Args:
    - winning_door (int): The door behind which the prize is placed.
    - selected_door (int): The door initially selected by the player.
    - change (bool): Flag to determine if the player changes their choice after a door is revealed.
    
    Returns:
    - bool: True if the player wins, False otherwise.
    """
    assert 0 <= winning_door < 3
    assert 0 <= selected_door < 3

    # Determine the remaining doors after removing the selected and winning doors
    remaining_doors = [door for door in range(3) if door != selected_door and door != winning_door]
    removed_door = random.choice(remaining_doors)

    # If change is True, select the other unopened door; otherwise, stick with the original choice
    if change:
        selected_door = [door for door in range(3) if door != selected_door and door != removed_door][0]

    return selected_door == winning_door

if __name__ == '__main__':
    total_trials = 1000000  # Number of trials to run the simulation
    player_doors = [random.randint(0, 2) for _ in range(total_trials)]  # Randomly select doors for each trial

    # Calculate the winning percentage without changing the initial choice
    winning_no_change = sum(game(1, door) for door in player_doors)
    print(f"Winning percentage without changing choice: {winning_no_change / total_trials * 100:.2f}%")

    # Calculate the winning percentage when changing the initial choice after a door is revealed
    winning_change = sum(game(1, door, change=True) for door in player_doors)
    print(f"Winning percentage while changing choice: {winning_change / total_trials * 100:.2f}%")
