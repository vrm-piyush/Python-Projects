# Card Game Program

## Project Overview

The Card Game Program is a Python application that simulates a card game involving players and a deck of cards. The program provides a range of features, including different player classes, game modes, and user interaction. It supports player-vs-player and player-vs-AI scenarios, allowing users to play rounds, save and load game states, and customize opponents and game modes.

## Features

- **Card Class:**

  - Represents a playing card with rank, suit, and points.
  - Provides comparison methods for sorting.

- **Deck Class:**

  - Generates and shuffles a deck of cards.
  - Deals cards to players.

- **Player Classes:**

  - Player: Represents a human player.
  - EasyAIPlayer: Simple AI player.
  - MediumAIPlayer: AI player with medium difficulty.
  - HardAIPlayer: AI player with high difficulty.

- **Game Class:**

  - Manages the game flow and rules.
  - Supports different game modes and opponents.
  - Displays game state and results.

- **Animation:**

  - Includes a basic card-drawing animation.

- **Save/Load:**

  - Allows saving and loading of the game state using pickle.

- **User Interaction:**

  - Users can choose opponents, game modes, and decide to quit or save during the game.

- **Game Modes:**

  - Supports "Best of Three" and "Sudden Death" game modes.

- **Player Customization:**

  - Users can input names for Player 1 and Player 2.
  - Choose opponents, game modes, and save/load game states.

- **Round Interaction:**

  - Users can initiate each round, draw cards, and view the winner.

## How to Use

1. **Run the Script:**

   - Execute the script to start the card game.

2. **Follow On-Screen Instructions:**

   - Enter player names, select opponents, and choose game modes.
   - Press 'q' to quit, 'Q' to exit, or any other key to play rounds.

3. **Save/Load Game State:**

   - Save the game state during gameplay.
   - Load a previously saved game state.

4. **Game Modes:**

   - Choose between "Best of Three" and "Sudden Death" modes.

5. **Player Interaction:**

   - View the current state of the game, including remaining cards in the deck.
   - Decide whether to save or load the game before exiting.

## Example

```bash
cd CardGameProgram
python card_game.py
```

```python
Player 1 name: John
Select an opponent:
1. Easy AI
2. Medium AI
3. Hard AI
4. Player 2
Enter the number for the desired opponent: 2
Select the game mode:
1. Best of Three
2. Sudden Death
Enter the number for the desired game mode: 2
Do you want to load a saved game? (y/n): n

Beginning War!
Sudden Death Mode: The first player to win a round wins the game.
Press 'q' to quit or 'Q' to exit game. Any key to play a round:

Current State of the Game:
Remaining cards in the deck: 50
John: 0 wins, 0 points
Medium AI: 0 wins, 0 points

John drew 2 of spades, Medium AI drew 6 of clubs
Medium AI wins this round


Current State of the Game:
Remaining cards in the deck: 50
John: 0 wins, 2 points
Medium AI: 1 wins, 6 points

War is over. Medium AI wins!
Do you want to save the current game state? (y/n):
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/vrm-piyush/CardGameProgram.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd CardGameProgram
   ```

3. **Run the Script:**

   ```bash
   python card_game.py
   ```

## Features to be Added

- **User Interface (UI):**

   - Create a simple text-based UI to make interactions more user-friendly.
   - Display the current state of the game, including the cards remaining in the deck.

- **Game Statistics:**

   - Keep track of additional statistics, such as the average number of turns per round, the longest winning streak, or the most frequently drawn card.

- **Customizable Deck:**

   - Allow users to customize the deck, choosing specific suits or excluding certain cards.

- **Sound Effects:**

   - Add simple sound effects for actions like drawing cards, winning a round, or winning the game.

- **Animations:**

   - If you're working with a graphical interface, consider adding simple animations for card movements or other interactions.

Consider the complexity of each feature and choose those that align with the goals and scope of the card game program. Each feature can enhance usability and functionality, but their implementation complexity may vary.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements, encounter any issues, or want to add new features, please open an [issue](https://github.com/vrm-piyush/CardGameProgram/issues) or submit a pull request.

---
