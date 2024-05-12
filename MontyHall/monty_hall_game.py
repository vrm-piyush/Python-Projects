# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Monty Hall Game Program.

Input:
- User input to choose the door for the prize.
- User input to decide whether to switch their choice after a door with a goat is revealed.

Output:
- A message indicating whether the user's choice results in a win or loss.

Features:
- Simulates the Monty Hall game with user interactions.
- Allows the user to choose a door, select the difficulty level, and decide whether to switch their choice.
- Displays game statistics, including wins and losses.
- Offers the option to play the game again.

"""

import random
import pygame

def play_monty(prize_door: int, selected_door: int, difficulty: str) -> int:
    """
    Simulates the Monty Hall game and returns the door opened by Monty.
    
    Args:
    - prize_door (int): The door behind which the prize is placed (0, 1, or 2).
    - selected_door (int): The initial door chosen by the player.
    
    Returns:
    - int: The door opened by Monty, revealing a goat.
    """

    # Intialize pygame mixer
    pygame.mixer.init()

    # Load the sound effect for revealing a goat
    goat_sound = pygame.mixer.Sound("goat_sound.wav")

    # Monty Hall reveals a door with a goat that isn't the selected door or the prize door
    doors_to_open = [door for door in range(3) if door != selected_door and door != prize_door]

    # Adjust difficulty level
    if difficulty == "easy":
        monty_opens = random.choice(doors_to_open)
    elif difficulty == "hard":
        monty_opens = random.choice(doors_to_open) if random.random() < 0.7 else prize_door
    else:
        raise ValueError("Invalid difficulty level! Please choose 'easy' or 'hard'.")
    
    print(f"\nMonty Hall opens door {monty_opens}, revealing a goat!")

    # Play the sound effect for revealing a goat
    goat_sound.play()
    
    return monty_opens

def main():
    """
    Main function to run the Monty Hall game.
    """

    wins = 0
    losses = 0

    print("\nWelcome to the Monty Hall Game!\n")
    
    while True:
        # Randomly select a door (0, 1, or 2) behind which the prize is placed
        prize_door = random.randint(0, 2)
        
        # Prompt the user to choose a door
        selected_door = int(input("Choose a door (0, 1, or 2): "))
        
        # Validate user input for the selected door
        while selected_door not in [0, 1, 2]:
            selected_door = int(input("Invalid choice! Please choose a door (0, 1, or 2): "))

        # Prompt the user to choose the difficulty level
        difficulty = input("Choose the difficulty level (easy/hard): ").strip().lower()
        
        # Validate user input for the difficulty level
        while difficulty not in ['easy', 'hard']:
            difficulty = input("Invalid difficulty level! Please choose 'easy' or 'hard': ").strip().lower()

        # Play the Monty Hall game and get the door opened by Monty
        monty_opens = play_monty(prize_door, selected_door, difficulty)

        # Ask the user if they want to switch their choice after Monty reveals a goat
        switch_choice = input("\nDo you want to switch your choice? (yes/no): ").strip().lower()
        
        # Validate user input for the switch choice
        while switch_choice not in ['yes', 'no']:
            switch_choice = input("Invalid input! Please enter 'yes' or 'no': ").strip().lower()
        
        # If the user chooses to switch, display the result
        if switch_choice == 'yes':
            remaining_door = [door for door in range(3) if door != selected_door and door != monty_opens][0]
            selected_door = remaining_door
        
        # Determine if the player's choice matches the prize door
        result = selected_door == prize_door

        print("\n--------------------------")
        print(f"Prize was behind door {prize_door}")
        print(f"You chose door {selected_door}")
        print(f"Monty Hall opened door {monty_opens}")
        
        
        if result:
            print("\nCongratulations! You've won the prize!")
            wins += 1
        else:
            print("\nSorry, you didn't win this time.")
            losses += 1
        
        # Display game statistics
        print(f"\nStatistics: Wins - {wins}, Losses - {losses}")
        
        # Ask the user if they want to play again
        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        
        if play_again != 'yes':
            break

if __name__ == "__main__":
    main()