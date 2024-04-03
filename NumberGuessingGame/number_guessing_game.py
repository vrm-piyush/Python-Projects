"""
Number Guessing Game Program.

Input:
- User interaction to choose difficulty, mode, and input guesses.
- Player names for high score board.

Output:
- Game statistics, high score board, and prompts for next game.

Features:
- Implements a Number Guessing Game with options to choose difficulty levels and game modes.
- Supports single-player and multiplayer modes, where players take turns guessing in multiplayer.
- Keeps track of high scores, displaying the top entries on the high score board.
- Allows players to input their names for the high score board.
- Provides statistics such as success rate and average attempts after playing rounds.
- Time limit for each round prevents unlimited thinking time.
- Offers an option to play again with a new set of difficulty and mode choices.

"""

import random
import time

class NumberGuessingGame:
    def __init__(self):
        self.score = 0
        self.high_scores = []
        self.difficulty_levels = {
            1: {'easy': (1, 10, 10)},
            2: {'medium': (1, 50, 20)},
            3: {'hard': (1, 100, 30)}
        }
        self.current_range = self.difficulty_levels[1]['easy']
        self.time_limit = 0
        self.multiplayer = False

    def choose_difficulty(self):
        """Prompt the user to choose the difficulty level for the game."""
        print("\nChoose difficulty:")
        for level, options in self.difficulty_levels.items():
            print(f"- {level}: {list(options.keys())[0].capitalize()}")

        try:
            chosen_difficulty = int(input("Enter difficulty level: "))
            if chosen_difficulty in self.difficulty_levels:
                difficulty_name, (start, end, time_limit) = next(iter(self.difficulty_levels[chosen_difficulty].items()))
                self.current_range = (start, end)
                self.time_limit = time_limit
                print(f"\nDifficulty set to {difficulty_name.capitalize()}.\n")
            else:
                print("Invalid difficulty level. Setting to Easy by default.\n")
        except ValueError:
            print("Invalid input! Please enter a number.\n")
            self.choose_difficulty()

    def choose_mode(self):
        """Prompt the user to choose the game mode (single or multiplayer)."""
        print("\nChoose mode:")
        print("- 1: Single Player")
        print("- 2: Multiplayer")

        try:
            chosen_mode = int(input("Enter mode: "))
            if chosen_mode == 2:
                self.multiplayer = True
                print("\nMultiplayer mode enabled. Players will take turns guessing.\n")
            elif chosen_mode != 1:
                print("Invalid mode. Single player mode enabled.\n")
        except ValueError:
            print("Invalid input! Please enter a number.\n")
            self.choose_mode()

    def play_game(self):
        """Main function to play the Number Guessing Game."""
        while True:
            self.scores = []  # Reset scores for each round

            self.choose_difficulty()
            self.choose_mode()

            for _ in range(2 if self.multiplayer else 1):  # Play multiple rounds in multiplayer mode
                self.play_round()

            self.display_statistics()

            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != 'yes':
                break

    def play_round(self):
        """Play a single round of the Number Guessing Game."""
        n = random.randrange(self.current_range[0], self.current_range[1] + 1)
        attempts = 0
        start_time = time.time()

        print("\nWelcome to the Number Guessing Game!")

        while True:
            try:
                guess = int(input("Enter your guess: "))
                attempts += 1

                if guess < n:
                    print("Too low! Try again.")
                elif guess > n:
                    print("Too high! Try again.")
                else:
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    if elapsed_time > self.time_limit:
                        print("Sorry, you ran out of time!")
                        self.scores.append(0)
                    else:
                        print(f"Congratulations! You guessed it right in {attempts} attempts.")
                        self.scores.append(attempts)

                    break  # Exit the loop for single player mode
            except ValueError:
                print("Invalid input! Please enter a number.\n")

        self.update_high_scores()

    def update_high_scores(self):
        """Update the high scores based on the current round's results."""
        if self.scores:
            try:
                average_score = sum(self.scores) / len(self.scores)
                print(f"\nAverage Score for this round: {average_score:.2f}\n")

                name = input("Enter your name for the high score board: ")

                current_score = average_score if self.multiplayer else self.scores[0]

                player_entry = next((player for player in self.high_scores if player['name'] == name), None)

                if player_entry:
                    if current_score > player_entry['score']:
                        player_entry['score'] = current_score
                        print(f"Congratulations! Your high score has been updated to {current_score:.2f} points.")
                    else:
                        print(f"Your previous high score is {player_entry['score']:.2f} points. No update needed.")
                else:
                    self.high_scores.append({'name': name, 'score': current_score})
                    print(f"Congratulations! You've been added to the high score board with {current_score:.2f} points.")

                self.high_scores.sort(key=lambda x: x['score'], reverse=True)

                print("\nHigh Score Board:")
                for i, high_score in enumerate(self.high_scores[:5], start=1):
                    print(f"{i}. {high_score['name']} - {high_score['score']:.2f} points")
            except ValueError:
                print("Invalid input! Please enter a valid name.\n")

    def display_statistics(self):
        """Display game statistics after playing the rounds."""
        if self.scores:
            success_rate = (self.scores.count(0) / len(self.scores)) * 100
            average_attempts = sum(self.scores) / len(self.scores)

            print(f"\nStatistics:")
            print(f"Success Rate: {success_rate:.2f}%")
            print(f"Average Number of Attempts: {average_attempts:.2f}")

if __name__ == '__main__':
    # Create an instance of the NumberGuessingGame and start playing
    game = NumberGuessingGame()
    game.play_game()