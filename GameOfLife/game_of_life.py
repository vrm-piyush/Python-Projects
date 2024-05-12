# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Conway's Game of Life Program.

Input:
- No direct input from the user required.

Output:
- Displays the evolution of a cellular automaton based on predefined rules.

Features:
- Initializes the game board with random cell values.
- Draws the game board based on the current cell values using Pygame.
- Applies the rules of Conway's Game of Life to evolve the board to the next generation.
- Continuously updates and displays the board, creating the simulation.

"""

# Importing necessary libraries
from typing import List
import pygame
import random
import time

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 60, 60
CELL_SIZE = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

def initialize_board() -> List[List[int]]:
    """
    Initialize the game board with random cell values.
    
    Returns:
    - List[List[int]]: 2D list representing the game board.
    """
    return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(board: List[List[int]]) -> None:
    """
    Draw the game board based on the current cell values.
    
    Args:
    - board (List[List[int]]): 2D list representing the game board.
    """
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if board[row][col] == 0 else GREEN
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

def game_of_life(board: List[List[int]]) -> None:
    """
    Apply the rules of Conway's Game of Life to evolve the board to the next generation.
    
    Args:
    - board (List[List[int]]): 2D list representing the game board.
    """
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    rows, cols = len(board), len(board[0])
    copy_board = [[board[row][col] for col in range(cols)] for row in range(rows)]

    for row in range(rows):
        for col in range(cols):
            live_neighbors = sum(copy_board[row + dr][col + dc] for dr, dc in neighbors if 0 <= row + dr < rows and 0 <= col + dc < cols)

            if copy_board[row][col] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                board[row][col] = 0
            elif copy_board[row][col] == 0 and live_neighbors == 3:
                board[row][col] = 1

if __name__ == '__main__':
    board = initialize_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game_of_life(board)
        draw_board(board)
        time.sleep(0.1)
    
    pygame.quit()