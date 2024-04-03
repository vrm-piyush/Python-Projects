"""
Rock, Paper, Scissors Game Program.

Input:
- User's choice among Rock, Paper, and Scissors. 
  They can also choose 'End' to exit the game.

Output:
- Results of each round and final scores.

Features:
- Offers a choice between Single Player Mode and Multiplayer Mode.
- In Single Player Mode, allows the player to select a difficulty level (easy, medium, hard).
- Implements an extended game with additional choices: Rock, Paper, Scissors, Lizard, Spock.
- Displays ASCII art for the extended game choices.
- Tracks and displays the historical statistics (Wins, Losses, Ties) in Single Player Mode.
- Allows players to reset scores at the end of each round or game.
- Handles input validation for user choices.
"""

import random
from collections import Counter

# Constants
CHOICES = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]
DIFFICULTY_LEVELS = {"easy": 0.2, "medium": 0.5, "hard": 0.8}
history_log = {"Wins": 0,"Losses": 0}

def print_game_choices():
    """Print ASCII art for extended game choices."""
    print("\nRock")
    print("   _______")
    print("--'   ____)")
    print("      (_____)")
    print("      (_____)")
    print("      (____)")
    print("---.__(___)")

    print("\nPaper")
    print("    _______")
    print("---'   ____)____")
    print("          ______)")
    print("          _______)")
    print("         _______)")
    print("---.__________)")

    print("\nScissors")
    print("    _______")
    print("---'   ____)____")
    print("          ______)")
    print("       __________)")
    print("      (____)")
    print("---.__(___)")

    print("Choose one of the following:")
    for i, choice in enumerate(CHOICES, start=1):
        print(f"{i}. {choice}")
    print("Type 'End' to exit the game.")

def get_user_choice():
    """Get a valid choice from the user."""
    while True:
        print_game_choices()
        choice = input("Enter your choice: ").capitalize()
        if choice in CHOICES or choice == 'End':
            return choice
        print("Invalid choice. Please enter the number of your choice or 'End.'")

def determine_winner(player, computer):
    """Determine the winner and return the outcome message."""
    if player == computer:
        return "Tie!", "tie"
    elif (
        (player == "Rock" and (computer == "Scissors" or computer == "Lizard"))
        or (player == "Scissors" and (computer == "Paper" or computer == "Lizard"))
        or (player == "Paper" and (computer == "Rock" or computer == "Spock"))
        or (player == "Lizard" and (computer == "Spock" or computer == "Paper"))
        or (player == "Spock" and (computer == "Scissors" or computer == "Rock"))
    ):
        return f"You win!!! {player} beats {computer}", "win"
    else:
        return f"You lose...! {computer} beats {player}", "lose"

def print_scores(round_number, cpu_score, player_score, ties):
    """Print the current scores and round number."""
    print(f"\nRound {round_number} Scores:")
    print(f"CPU: {cpu_score}")
    print(f"Player: {player_score}")
    print(f"Ties: {ties}")

def reset_scores():
    """Reset scores to zero."""
    return 0, 0, 0

def multiplayer_mode():
    """Play in multiplayer mode."""
    print("\nWelcome to Multiplayer Mode!")
    player1_name = input("Enter Player 1's name: ")
    player2_name = input("Enter Player 2's name: ")

    player1_score, player2_score, ties = 0, 0, 0
    round_number = 1

    while True:
        player1 = get_user_choice()
        if player1 == 'End':
            print(f"\nFinal Scores for {player1_name} and {player2_name}:")
            print(f"{player1_name}: {player1_score}")
            print(f"{player2_name}: {player2_score}")
            print(f"Ties: {ties}")
            break

        player2 = get_user_choice()
        if player2 == 'End':
            print(f"\nFinal Scores for {player1_name} and {player2_name}:")
            print(f"{player1_name}: {player1_score}")
            print(f"{player2_name}: {player2_score}")
            print(f"Ties: {ties}")
            break

        outcome = determine_winner(player1, player2)
        print(outcome[0])

        if "win" in outcome[1]:
            player1_score += 1
        elif "lose" in outcome[1]:
            player2_score += 1
        else:
            ties+=1

        # Print scores after each round in multiplayer mode
        print_multiplayer_scores(round_number, player1_name, player1_score, player2_name, player2_score, ties)
        round_number += 1

        # Ask if the players want to reset scores
        reset_option = input("\nDo you want to reset scores? (y/n): ").lower()
        if reset_option == 'y':
            player1_score, player2_score, ties = reset_scores()
            print("\nScores reset to zero. Starting a new game.")
            round_number = 1

def print_multiplayer_scores(round_number, player1_name, player1_score, player2_name, player2_score, ties):
    """Print the scores for each round in multiplayer mode."""
    print(f"\nRound {round_number} Scores:")
    print(f"{player1_name}: {player1_score}")
    print(f"{player2_name}: {player2_score}")
    print(f"Ties: {ties}")

def single_player_mode(difficulty_level):
    """Play in single-player mode against a computer opponent."""
    print(f"\nWelcome to Single Player Mode (Difficulty: {difficulty_level.capitalize()})!")
    
    player_score, cpu_score, ties = 0, 0, 0
    round_number = 1

    while True:
        player = get_user_choice()
        if player == 'End':
            print('\nFinal Scores:')
            print(f"CPU: {cpu_score}")
            print(f"Player: {player_score}")
            print(f"Ties: {ties}")
            break

        computer = get_computer_choice(difficulty_level, player)
        outcome = determine_winner(player, computer)
        print(outcome[0])

        if "win" in outcome[1]:
            player_score += 1
        elif "lose" in outcome[1]:
            cpu_score += 1
        else:
            ties += 1

        # Print scores after each round
        print_scores(round_number, cpu_score, player_score, ties)
        round_number += 1

        # Update history log for single-player mode
        update_history_log(outcome[1])

        # Ask if the user wants to reset scores
        reset_option = input("\nDo you want to reset scores? (y/n): ").lower()
        if reset_option == 'y':
            player_score, cpu_score, ties = reset_scores()
            print("\nScores reset to zero. Starting a new game.")
            round_number = 1
    
    display_single_player_history_log(history_log)

def update_history_log(outcome):
    """Update the history log based on the outcome of the current round."""
    global history_log
    if outcome == "win":
        history_log['Wins'] += 1
    elif outcome == "lose":
        history_log['Losses'] += 1
    else:
        history_log['Ties'] += 1

def get_computer_choice(difficulty_level, player_choice):
    """Get the computer's choice based on difficulty level."""
    if difficulty_level == "easy":
        return random.choice(CHOICES)
    elif difficulty_level == "medium":
        # Medium difficulty: Computer makes a slightly biased choice
        return random.choices(CHOICES, weights=[0.3, 0.3, 0.3, 0.05, 0.05])[0]
    elif difficulty_level == "hard":
        # Hard difficulty: Computer makes a more strategic choice
        if random.random() < 0.8:
            return get_best_choice(player_choice)
        else:
            return random.choice(CHOICES)


def get_best_choice(player_choices):
    """Get the computer's best choice based on the player's historical choices."""
    if not player_choices:
        # If no player choices are available, choose a random option
        return random.choice(CHOICES)

    # Count the occurrences of each choice made by the player
    choices_count = Counter(player_choices)

    # Find the most common choice made by the player
    most_common_choice = choices_count.most_common(1)[0][0]

    # Determine the choice that beats the most common choice made by the player
    choices_beating_most_common = {
        "Rock": "Paper",
        "Paper": "Scissors",
        "Scissors": "Rock",
        "Lizard": "Scissors",
        "Spock": "Lizard"
    }

    # Choose the option that beats the most common choice or a random choice if there is a tie
    computer_choice = choices_beating_most_common.get(most_common_choice, random.choice(CHOICES))

    return computer_choice

def display_single_player_history_log(history_log):
    """Display the historical statistics for single-player mode."""
    print("\nSingle Player History Log:")
    print(f"Wins: {history_log['Wins']}")
    print(f"Losses: {history_log['Losses']}")
    print(f"Ties: {history_log['Ties']}")

if __name__ == '__main__':
    history_log = {"Wins": 0, "Losses": 0, "Ties": 0}

    print("Welcome to Rock, Paper, Scissors, Lizard, Spock Game!")
    print("Select a mode:")
    print("1. Single Player Mode")
    print("2. Multiplayer Mode")
    mode_choice = input("Enter the number of your choice: ")

    if mode_choice == '1':
        difficulty_level = input("Select difficulty level by entering the number (easy, medium, hard): ").lower()
        single_player_mode(difficulty_level)

    elif mode_choice == '2':
        multiplayer_mode()

    else:
        print("Invalid choice. Exiting the game.")