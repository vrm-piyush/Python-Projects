"""
Chessboard Program.

Output:
- Chessboard.

Features:
- GUI for displaying a chessboard.
- Ability to place and move chess pieces.
- Customizable colors for light squares, dark squares, and selected squares.
- Save and load board states.
- Initial placement of standard chess pieces (pawns, rooks, knights, bishops, queens, and kings).
- Support for saving and loading the board state to/from a file.
- Customization of chessboard colors using user-defined color codes.

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

class Chessboard:
    def __init__(self, size=8):
        """
        Initialize the Chessboard.

        Args:
        - size (int): Size of the chessboard (default is 8).
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.fig, self.ax = plt.subplots()
        self.selected_square = None
        self.customization = {
            'light_color': '#f0d9b5',  # Light squares (beige)
            'dark_color': '#b58863',   # Dark squares (darker brown)
            'selected_color': '#add8e6'  # Selected squares (light blue)
        }

        self.piece_symbols = {
            1: '♙',  # Pawn (white)
            2: '♖',  # Rook (white)
            3: '♘',  # Knight (white)
            4: '♗',  # Bishop (white)
            5: '♕',  # Queen (white)
            6: '♔',  # King (white)
            -1: '♟',  # Pawn (black)
            -2: '♜',  # Rook (black)
            -3: '♞',  # Knight (black)
            -4: '♝',  # Bishop (black)
            -5: '♛',  # Queen (black)
            -6: '♚'   # King (black)
        }

    def draw_chessboard(self):
        """
        Draw the chessboard with customizable colors and piece placements.
        """
        light_color = self.customization['light_color']
        dark_color = self.customization['dark_color']
        selected_color = self.customization['selected_color']

        for i in range(self.size):
            for j in range(self.size):
                color = light_color if (i + j) % 2 == 0 else dark_color
                if self.selected_square and (i, j) == self.selected_square:
                    color = selected_color
                self.ax.add_patch(Rectangle((i, j), 1, 1, fill=True, color=color))
                if self.board[i, j] != 0:
                    self.ax.text(i + 0.5, j + 0.5, self.piece_symbols[self.board[i, j]],
                                 fontsize=20, ha='center', va='center')

        # Add chess notation labels
        for i in range(self.size):
            self.ax.text(i + 0.5, -0.5, chr(ord('a') + i), ha='center', va='center', fontsize=10)
            self.ax.text(-0.5, i + 0.5, str(self.size - i), ha='center', va='center', fontsize=10)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(0, self.size)
        self.ax.set_ylim(0, self.size)

    def on_click(self, event):
        """
        Handle mouse click events on the chessboard.
        """
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)
            if self.selected_square == (x, y):
                self.selected_square = None
            else:
                self.selected_square = (x, y)
            self.draw_chessboard()
            plt.draw()

    def place_piece(self, row, col, piece):
        """
        Place a chess piece on the board.

        Args:
        - row (int): Row index.
        - col (int): Column index.
        - piece (int): Piece identifier.
        """
        self.board[row, col] = piece
        self.draw_chessboard()
        plt.draw()
        
    def place_initial_pieces(self):
        for i in range(self.size):
            self.place_piece(1, i, 1)   # White pawns
            self.place_piece(self.size - 2, i, -1)   # Black pawns

            if i == 0 or i == self.size - 1:
                self.place_piece(0, i, 2)   # White rooks
                self.place_piece(self.size - 1, i, -2)   # Black rooks
            elif i == 1 or i == self.size - 2:
                self.place_piece(0, i, 3)   # White knights
                self.place_piece(self.size - 1, i, -3)   # Black knights
            elif i == 2 or i == self.size - 3:
                self.place_piece(0, i, 4)   # White bishops
                self.place_piece(self.size - 1, i, -4)   # Black bishops
            elif i == 3:
                self.place_piece(0, i, 5)   # White queen
                self.place_piece(self.size - 1, i, -5)   # Black queen
            elif i == self.size - 4:
                self.place_piece(0, i, 6)   # White king
                self.place_piece(self.size - 1, i, -6)   # Black king

    def customize_chessboard(self, light_color, dark_color, selected_color):
        """
        Customize the colors of the chessboard.

        Args:
        - light_color (str): Color code for light squares.
        - dark_color (str): Color code for dark squares.
        - selected_color (str): Color code for selected squares.
        """
        self.customization['light_color'] = light_color
        self.customization['dark_color'] = dark_color
        self.customization['selected_color'] = selected_color
        self.draw_chessboard()
        plt.draw()

    def save_board_state(self, filename):
        """
        Save the current board state to a file.

        Args:
        - filename (str): Name of the file to save the board state.
        """
        np.save(filename, self.board)
        print(f"Board state saved to {filename}")

    def load_board_state(self, filename):
        """
        Load a board state from a file.

        Args:
        - filename (str): Name of the file containing the board state.
        """
        try:
            loaded_board = np.load(filename)
            if loaded_board.shape == (self.size, self.size):
                self.board = loaded_board
                self.draw_chessboard()
                plt.draw()
            else:
                print(f"Invalid board size in file {filename}. Board not loaded.")
        except Exception as e:
            print(f"Error loading board state from {filename}: {e}")

    def on_key(self, event):
        """
        Handle keyboard events.

        Args:
        - event: Keyboard event.
        """
        if event.key.lower() == 's':
            self.save_board_state("saved_board.npy")
        elif event.key.lower() == 'l':
            self.load_board_state("saved_board.npy")
        elif event.key.lower() == 'c':
            light_color = input("Enter light color (e.g., white): ")
            dark_color = input("Enter dark color (e.g., black): ")
            selected_color = input("Enter selected color (e.g., yellow): ")
            self.customize_chessboard(light_color, dark_color, selected_color)

    def run(self):
        """
        Run the chessboard application.
        """
        self.draw_chessboard()
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        plt.show()

if __name__ == '__main__':
    chessboard = Chessboard(size=8)
    chessboard.place_initial_pieces()  # Place initial chess pieces
    chessboard.save_board_state("saved_board.npy")  # Save board state
    chessboard.load_board_state("saved_board.npy")  # Load board state
    chessboard.run()