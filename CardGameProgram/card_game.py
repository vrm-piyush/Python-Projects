"""
Card Game Program.

Input:
- User input to proceed with each round of the game.

Output:
- Displays the winner of each round and the final scores at the end.

Features:
- Card Class:
   - Represents a playing card with rank, suit, and points.
   - Provides comparison methods for sorting.

- Deck Class:
   - Generates and shuffles a deck of cards.
   - Deals cards to players.

- Player Classes:
   - Player: Represents a human player.
   - EasyAIPlayer: Simple AI player.
   - MediumAIPlayer: AI player with medium difficulty.
   - HardAIPlayer: AI player with high difficulty.

- Game Class:
   - Manages the game flow and rules.
   - Supports different game modes and opponents.
   - Displays game state and results.

- Animation:
   - Includes a basic card-drawing animation.

- Save/Load:
   - Allows saving and loading of the game state using pickle.

- User Interaction:
   - Users can choose opponents, game modes, and decide to quit or save during the game.

Usage:
- Run the script to play the card game. class to manage the overall game, deal cards, and determine the winner of each round.

"""
import os
import time
import pickle
from random import shuffle, choice

class Card:
    suits = ['spades', 'hearts', 'diamonds', 'clubs']
    rank_names = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace', 'Joker']
    point_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 10, 'Joker': 0}

    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit
        self.points = self.point_values[self.rank_names[rank]]

    def __lt__(self, c2):
        if self.rank < c2.rank:
            return True
        if self.rank == c2.rank:
            return self.suit < c2.suit
        return False

    def __gt__(self, c2):
        return not self.__lt__(c2)

    def __repr__(self) -> str:
        return f"{self.rank_names[self.rank]} of {self.suits[self.suit]}"

class Deck:
    def __init__(self) -> None:
        self.cards = [Card(rank, suit) for rank in range(2, 15) for suit in range(4)]
        shuffle(self.cards)

    def deal_card(self):
        """Deal a card from the deck."""
        if self.cards:
            return self.cards.pop()

class Player:
    def __init__(self, name, profile=None) -> None:
        self.wins = 0
        self.points = 0
        self.card = None
        self.name = name

class EasyAIPlayer(Player):
    def make_decision(self):
        return self.card

class MediumAIPlayer(Player):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.hand = []

    def make_decision(self, opponent_card):
        if self.card > opponent_card:
            return self.card
        else:
            return choice([card for card in self.hand if card != self.card])

class HardAIPlayer(Player):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.hand = []

    def make_decision(self, opponent_card):
        if self.card > opponent_card:
            return self.card
        else:
            return min(self.hand)

class Game:
    def __init__(self) -> None:
        self.deck = Deck()
        self.p1 = Player(input("Player 1 name: "))
        self.p2 = self.select_opponent()
        self.rounds = 3
        self.mode = self.select_game_mode()

    def select_opponent(self):
        print("Select an opponent:")
        print("1. Easy AI")
        print("2. Medium AI")
        print("3. Hard AI")
        print("4. Player 2")

        while True:
            choice_opponent = input("Enter the number for the desired opponent: ")

            if choice_opponent == '1':
                return EasyAIPlayer("Easy AI")
            elif choice_opponent == '2':
                return MediumAIPlayer("Medium AI")
            elif choice_opponent == '3':
                return HardAIPlayer("Hard AI")
            elif choice_opponent == '4':
                return Player(input("Player 2 name: "))
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    def select_game_mode(self):
        print("Select the game mode:")
        print("1. Best of Three")
        print("2. Sudden Death")

        while True:
            choice_mode = input("Enter the number for the desired game mode: ")

            if choice_mode == '1':
                return "Best of Three"
            elif choice_mode == '2':
                return "Sudden Death"
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def display_winner(self, winner_name):
        print(f"{winner_name} wins this round\n")

    def display_draw(self, p1_name, p1_card, p2_name, p2_card):
        print(f"{p1_name} drew {p1_card}, {p2_name} drew {p2_card}")

    def display_state(self):
        print("\nCurrent State of the Game:")
        print(f"Remaining cards in the deck: {len(self.deck.cards)}")
        print(f"{self.p1.name}: {self.p1.wins} wins, {self.p1.points} points")
        print(f"{self.p2.name}: {self.p2.wins} wins, {self.p2.points} points\n")

    def play_round(self):
        n = self.rounds if self.mode == "Best of Three" else 1
        for _ in range(n):
            response = input("Press 'q' to quit or 'Q' to exit game. Any key to play a round: ")

            if response == 'q':
                break
            elif response == 'Q':
                exit()

            p1_card = self.deck.deal_card()
            p2_card = self.deck.deal_card()

            if p1_card is not None and p2_card is not None:
                self.animate_card_draw(p1_card, p2_card)
                self.display_draw(self.p1.name, p1_card, self.p2.name, p2_card)

                if p1_card.points > p2_card.points:
                    self.p1.wins += 1
                    self.p1.points += p1_card.points
                    self.p2.points += p2_card.points
                    self.display_winner(self.p1.name)
                elif p1_card.points == p2_card.points:
                    print("It's a draw!")                    
                else:
                    self.p2.wins += 1
                    self.p1.points += p1_card.points
                    self.p2.points += p2_card.points
                    self.display_winner(self.p2.name)

                self.display_state()

    def animate_card_draw(self, p1_card, p2_card):
        for _ in range(5):
            os.system("clear" if os.name == 'posix' else 'cls')
            print("Drawing cards...")
            time.sleep(0.2)

        os.system("clear" if os.name == 'posix' else 'cls')
        self.display_state()  # Display state after animation

    def calculate_points(self):
        self.p1.points = sum(card.points for card in self.deck.cards)
        self.p2.points = sum(card.points for card in self.deck.cards)

    def play_game(self):
        print("\nBeginning War!")
        if self.mode == "Sudden Death":
            print("Sudden Death Mode: The first player to win a round wins the game.")
            self.play_sudden_death()
        else:
            print(f"{self.mode} Mode: The first player to win {self.rounds} rounds wins the game.")
            self.play_round()

        self.calculate_points()
        winner_name = self.winner(self.p1, self.p2)
        print(f"War is over. {winner_name} wins!")

    def play_sudden_death(self):
        while True:
            self.play_round()

            if self.p1.wins == 1 or self.p2.wins == 1:
                break

    def winner(self, p1, p2):
        """Determine the winner of the game."""
        if p1.wins > p2.wins:
            return p1.name
        if p1.wins < p2.wins:
            return p2.name
        return "It was a tie!"

    def display_final_scores(self):
        """Display the final scores of the players."""
        print(f"\nFinal Scores:\n{self.p1.name}: {self.p1.wins}\n{self.p2.name}: {self.p2.wins}")

    def save_game_state(self, file_name='game_state.pickle'):
        game_state = {
            'deck': self.deck,
            'p1': self.p1,
            'p2': self.p2,
            'rounds': self.rounds,
            'mode': self.mode
        }

        with open(file_name, 'wb') as file:
            pickle.dump(game_state, file)
        print(f"Game state saved to {file_name}")

    def load_game_state(self, file_name='game_state.pickle'):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                game_state = pickle.load(file)

            self.deck = game_state['deck']
            self.p1 = game_state['p1']
            self.p2 = game_state['p2']
            self.rounds = game_state['rounds']
            self.mode = game_state['mode']

            print(f"Game state loaded from {file_name}")
        else:
            print(f"No game state found at {file_name}")

if __name__ == '__main__':
    game = Game()

    # Ask the user if they want to load a saved game
    load_saved_game = input("Do you want to load a saved game? (y/n): ").lower()
    if load_saved_game == 'y':
        game.load_game_state()

    game.play_game()

    # Ask the user if they want to save the game before exiting
    save_game = input("Do you want to save the current game state? (y/n): ").lower()
    if save_game == 'y':
        game.save_game_state()

    game.display_final_scores()