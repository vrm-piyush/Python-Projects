"""
Settings for the Snake Game

- Define constants for the game
- Set up logging to a file named 'snake.log'
- Define color themes for the game
- Define control schemes for the game
- Define paths to various game assets
- Define the size and opacity of the shadow effect
- Define the starting length and position of the snake
- Define the window dimensions and frames per second (FPS)
- Define the paths to various game assets

"""

from pygame.locals import *
import pygame
from sys import exit
from os.path import join
import random
import time
import logging

# Set up logging to a file named 'snake.log'
log_filename = 'snake.log'
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
    ]
)

# Define constants for the game
CELL_SIZE = 80
ROWS = 11
COLS = 16
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

FPS = 60

START_LENGTH = 3
START_ROW = ROWS // 2
START_COL = START_LENGTH + 2

SHADOW_SIZE = pygame.Vector2(4,4)
SHADOW_OPACITY = 50

# Paths to various game assets
BACKGROUND_IMAGE_PATH = 'Graphics/background_image.png'
SETTINGS_BACKGROUND_IMAGE_PATH = 'Graphics/settings_bg_image.png'
HELP_BACKGROUND_IMAGE_PATH = 'Graphics/help_bg_image.png'
FONT_PATH = 'Font/PoetsenOne-Regular.ttf'
GAME_ICON_PATH = 'Graphics/snake_icon.png'
OBSTACLE_IMAGE_PATH = 'Graphics/obstacle.png'
SETTINGS_ICON_PATH = 'Graphics/settings_icon.png'
HOME_ICON_PATH = 'Graphics/home_icon.png'
HELP_ICON_PATH = 'Graphics/help_icon.png'
X_ICON_PATH = 'Graphics/x_icon.png'
PAUSE_ICON_PATH = 'Graphics/resume_pause_icon.png'
RESUME_BTN_ICON_PATH = 'Graphics/resume_btn_icon.png'
PLAY_ICON_PATH = 'Graphics/play_icon.png'

# Color themes for the game
# Modify color theme definitions
CLASSIC_THEME = {
    'background': (137, 206, 148),      # Light green
    'board_light': (170, 215, 81),      # Light green
    'board_dark': (162, 209, 61),       # Dark green
    'font_color': (254, 215, 76),       # Yellow
    'info_color': (0, 0, 0),            # Black
}

DARK_MODE_THEME = {
    'background': (37, 38, 39),         # Dark gray
    'board_light': (30, 30, 30),        # Darker gray
    'board_dark': (50, 50, 50),         # Darkest gray
    'font_color': (255, 255, 255),      # White
    'info_color': (0, 255, 255),        # Cyan
}

VIBRANT_THEME = {
    'background': (151, 99, 145),       # Pomp and Power    
    'board_light': (116, 187, 251),     # Light blue
    'board_dark': (0, 169, 165),        # Dark blue
    'font_color': (169, 255, 247),      # Light blue
    'info_color': (42, 12, 78),         # Naples yellow
}

VIOLET_BLUE_THEME = {
    'background': (45, 137, 139),       # Dark cyan
    'board_light': (184, 184, 255),     # Periwinkle
    'board_dark': (147, 129, 255),      # Tropical indigo
    'font_color': (59, 31, 43),         # Dark Purple
    'info_color': (255, 255, 255),      # White
}

VINTAGE_THEME = {
    'background': (232, 172, 101),      # Earth yellow
    'board_light': (255, 203, 105),     # Sunglow
    'board_dark': (208, 140, 96),       # Persian orange
    'font_color': (70, 63, 26),         # Drab dark brown
    'info_color': (255, 255, 255),      # White
}

# Control schemes for the game
# Control schemes
ARROW_KEYS = {
    'up': K_UP,
    'down': K_DOWN,
    'left': K_LEFT,
    'right': K_RIGHT
}

WASD_KEYS = {
    'up': K_w, 
    'down': K_s, 
    'left': K_a, 
    'right': K_d
}

IJKL_KEYS = {
    'up': K_i, 
    'down': K_k, 
    'left': K_j, 
    'right': K_l
}


"""
The implementation of features can depend on the complexity you want to introduce to the game. Here's a suggested order for implementing the features:

1. Levels : Start by implementing multiple levels with increasing difficulty. Introduce basic obstacles or changes in the game environment to make each level unique.

2. Pause and Resume : Implement a pause feature to allow players to pause the game and resume later without losing progress. This is essential for a smooth gameplay experience.

3. Responsive Controls : Enhance the responsiveness of controls to ensure smooth and precise movement for the snake. Responsive controls are crucial for a satisfying gameplay experience.

4. Obstacles : Introduce obstacles that the snake must navigate around. This adds complexity to the gameplay and challenges players to strategize their movements.

5. Animations : Add more animations for special events, such as the snake growing longer, power-up pickups, or level transitions. Animations can enhance the visual appeal of the game.

6. Sound Effects : Expand the variety of sound effects based on different in-game events to make the experience more immersive. Sound effects contribute to the overall atmosphere of the game.

7. Power-ups : Introduce special items that can either help the snake or add challenges. This adds variability to the gameplay and keeps players engaged.

8. Randomized Apple Effects : Make the apple pickups more interesting by introducing randomized effects. This adds an element of surprise to the game.

9. Scoreboard : Create a persistent scoreboard to track and display high scores across different game sessions. This provides a competitive aspect to the game.

10. Settings Menu : Allow players to customize the game settings_text. Implement a settings_text menu where players can adjust sound volume, difficulty level, or choose different snake skins.

11. Game Over Screen : Create a more engaging game over screen with a summary of the player's performance. Encourage players to play again or share their scores.

12. Achievements and Rewards : Add achievements or rewards for completing specific challenges or reaching certain milestones. This gives players additional goals to strive for.

13. Customizable Snake : Allow players to customize the appearance of the snake with different colors, patterns, or accessories. This adds a personal touch to the gameplay.

14. Tutorial : Include a tutorial or guide for new players to understand the game mechanics and controls. This ensures that players can quickly grasp the basics.

15. Mobile Compatibility : Adapt the game for mobile devices with touch controls and an optimized user interface. This expands the potential audience for the game.

16. Multiplayer Mode : Consider implementing a local or online multiplayer mode where players can compete or cooperate in real-time. This is a more advanced feature that can be added later for a richer gaming experience.


Separation of Concerns:
Consider breaking down your Main class further. It's handling a lot of responsibilities, including game initialization, drawing, input handling, and more. Consider creating separate classes for these responsibilities (e.g., Game, InputHandler, etc.) to achieve better separation of concerns.

Code Comments:
Add comments to explain complex sections of your code. This will make it easier for others (or even yourself in the future) to understand the logic behind certain decisions or implementations.

Optimization:
Optimize your code where possible. For example, consider using a sprite group for managing your snake's body segments for better performance.

Error Handling:
Implement error handling to gracefully handle potential issues, providing feedback to the user.

Responsive Design:
Ensure that the game looks good and is playable on different screen sizes and resolutions.

Logging:
Consider adding logging to help with debugging and understanding the flow of your game.
"""