# Number Guessing Game Program

![Number Guess](image.png)

## Project Overview

The Number Guessing Game Program is a Python application that implements a classic number guessing game. It provides a text-based interface where users can choose difficulty levels, game modes, and input their guesses. The game supports both single-player and multiplayer modes, keeping track of high scores, displaying top entries on the high score board, and offering game statistics after playing rounds.

## Features

- **Difficulty Levels:**
  - Implement different difficulty levels (easy, medium, hard) with a varying range of numbers.

- **Game Modes:**
  - Single-player mode where a player guesses the number.
  - Multiplayer mode where players take turns guessing.

- **Hints:**
  - Provide hints after each incorrect guess, such as "Too high" or "Too low."

- **Score System:**
  - Introduce a scoring system based on the number of attempts. The fewer attempts, the higher the score.

- **Time Limit:**
  - Add a time limit for each guess to increase the challenge.

- **High Score Board:**
  - Keep track of the highest scores and display a leaderboard.

## How to Play

1. **Run the Program:**
   - Execute the program to start the Number Guessing Game.

2. **Choose Difficulty:**
   - Select the difficulty level (easy, medium, hard) for the game.

3. **Choose Mode:**
   - Choose the game mode (single-player or multiplayer).

4. **Guess the Number:**
   - Input your guess for the randomly generated number.

5. **Hints and Results:**
   - Receive hints after each incorrect guess and find out the results at the end of the round.

6. **High Score Board:**
   - Input your name to be added to the high score board based on your performance.

7. **Play Again:**
   - Decide if you want to play again with different difficulty and mode choices.

## Example

```bash
cd NumberGuessingGame
python number_guessing_game.py
```

```python
Choose difficulty:
- 1: Easy
- 2: Medium
- 3: Hard
Enter difficulty level: 1

Difficulty set to Easy.


Choose mode:
- 1: Single Player
- 2: Multiplayer
Enter mode: 1

Welcome to the Number Guessing Game!
Enter your guess: 5
Congratulations! You guessed it right in 1 attempts.

Average Score for this round: 1.00

Enter your name for the high score board: P
Congratulations! You have been added to the high score board with 1.00 points.

High Score Board:
1. P - 1.00 points

Statistics:
Success Rate: 0.00%
Average Number of Attempts: 1.00
Do you want to play again? (yes/no): no
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/vrm-piyush/NumberGuessingGame.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd NumberGuessingGame
   ```

3. **Run the Program:**

   ```bash
   python number_guessing_game.py
   ```

## Features to be Added

- **GUI:**
  - Create a graphical user interface using a library like Tkinter or Pygame for a more visually appealing game.

- **Sound Effects:**
  - Include sound effects for correct and incorrect guesses.

- **Customization:**
  - Allow users to customize game settings, such as background color, font, or difficulty.

- **Statistics:**
  - Display statistics, such as average number of attempts, success rate, etc.

- **Animations:**
  - Add animations for correct and incorrect guesses.

- **Number Range Selection:**
  - Let users choose the range of numbers they want to guess.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements, encounter any issues, or want to add new features, please open an [issue](https://github.com/vrm-piyush/NumberGuessingGame/issues) or submit a pull request.

---