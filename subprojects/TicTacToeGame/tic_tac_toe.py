# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Tic-Tac-Toe Game with GUI.

Input:
- Mouse click to place 'X' or 'O' on the board.

Output:
- Winner announcement or tie, and score update.

Features:
- Simulates a Tic-Tac-Toe game with a graphical user interface.
- Allows players to click on the board to place 'X' or 'O'.
- Displays winner announcements, tie results, and updates the score.
- Provides an option to play again by clicking on the board after a game ends.
- Exit button to close the game.

"""

import tkinter as tk
import numpy as np

SIZE_OF_BOARD = 800
SYMBOL_SIZE = (SIZE_OF_BOARD / 3 - SIZE_OF_BOARD / 8) / 2
SYMBOL_THICKNESS = 50
SYMBOL_X_COLOR = '#FF4035'
SYMBOL_O_COLOR = '#0492CF'
GREEN_COLOR = '#7BC043'

class Tic_Tac_Toe:
    def __init__(self) -> None:
        # Initialize the main game window and canvas
        self.window = tk.Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = tk.Canvas(self.window, width=SIZE_OF_BOARD, height=SIZE_OF_BOARD)
        self.canvas.pack()
        
        # Bind mouse click to game action
        self.window.bind('<Button-1>', self.click)

        # Game variables initialization
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        # Draw horizontal and vertical lines to create a 3x3 grid
        for i in range(2):
            self.canvas.create_line((i + 1) * SIZE_OF_BOARD / 3, 0, (i + 1) * SIZE_OF_BOARD / 3, SIZE_OF_BOARD)
            self.canvas.create_line(0, (i + 1) * SIZE_OF_BOARD / 3, SIZE_OF_BOARD, (i + 1) * SIZE_OF_BOARD / 3)

        # Exit button setup
        exit_button = tk.Button(self.window, text="Exit", font="Helvetica 20 bold", bg=GREEN_COLOR, fg='white', command=self.exit_game)
        exit_button.pack(side='bottom', fill='x')

    def play_again(self):
        """
        Reset the board for a new game.
        """
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    def draw_O(self, logical_position):
        """
        Draw the 'O' symbol on the canvas.
        """
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE,
                                grid_position[0] + SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, outline=SYMBOL_O_COLOR)

    def draw_X(self, logical_position):
        """
        Draw the 'X' symbol on the canvas.
        """
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE,
                                grid_position[0] + SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, fill=SYMBOL_X_COLOR)
        self.canvas.create_line(grid_position[0] - SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE,
                                grid_position[0] + SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, fill=SYMBOL_X_COLOR)

    def display_gameover(self):
        """
        Display the game result on the canvas.
        """
        # Determine the winner or if it's a tie
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = SYMBOL_X_COLOR
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = SYMBOL_O_COLOR
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        # Display the game result and scores
        self.canvas.delete('all')
        self.canvas.create_text(SIZE_OF_BOARD / 2, SIZE_OF_BOARD / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(SIZE_OF_BOARD / 2, 5 * SIZE_OF_BOARD / 8, font="cmr 40 bold", fill=GREEN_COLOR,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O) : ' + str(self.O_score) + '\n'
        score_text += 'Tie                : ' + str(self.tie_score)
        self.canvas.create_text(SIZE_OF_BOARD / 2, 3 * SIZE_OF_BOARD / 4, font="cmr 30 bold", fill=GREEN_COLOR,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(SIZE_OF_BOARD / 2, 15 * SIZE_OF_BOARD / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)
        
    def convert_logical_to_grid_position(self, logical_position):
        """
        Convert logical position to grid position.
        """
        logical_position = np.array(logical_position, dtype=int)
        return (SIZE_OF_BOARD / 3) * logical_position + SIZE_OF_BOARD / 6

    def convert_grid_to_logical_position(self, grid_position):
        """
        Convert grid position to logical position.
        """
        grid_position = np.array(grid_position)
        return np.array(grid_position // (SIZE_OF_BOARD / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        """
        Check if a grid position is occupied.
        """
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True
    
    def is_winner(self, player):
        """
        Check if the given player has won.
        """
        player = -1 if player == 'X' else 1

        # Check rows and columns for a win
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Check diagonals for a win
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True
        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):
        """
        Check if the game is a tie.
        """
        r, c = np.where(self.board_status == 0)
        if len(r) == 0:
            return True
        return False
    
    def is_gameover(self):
        """
        Check if the game is over (someone wins or it's a tie).
        """
        self.X_wins = self.is_winner('X')
        self.O_wins = self.is_winner('O')
        self.tie = self.is_tie()

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return self.X_wins or self.O_wins or self.tie

    def click(self, event):
        """
        Handle mouse click events on the canvas.
        """
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            # Player 'X' turn
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            # Player 'O' turn
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # Check if the game has ended
            if self.is_gameover():
                self.display_gameover()
        else:  # Reset the board for a new game
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def exit_game(self):
        """
        Close the game window.
        """
        self.window.destroy()

if __name__ == '__main__':
    # Start the game
    game_instance = Tic_Tac_Toe()
    game_instance.mainloop()