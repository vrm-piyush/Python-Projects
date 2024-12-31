"""
Settings for the SlitherQuest

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
import logging
import random
from os.path import join
import cv2

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

# Level progression data
LEVELS_DATA = [
    {
        "obstacles": [], 
        "speed": 200, 
        'score_to_advance': 10, 
        'level_obstacles': 0
    },
    {
        "obstacles": [], 
        "speed": 150, 
        'score_to_advance': 20, 
        'level_obstacles': 1
    },
    {
        "obstacles": [], 
        "speed": 120, 
        'score_to_advance': 35, 
        'level_obstacles': 2
    },
    {
        "obstacles": [], 
        "speed": 100, 
        'score_to_advance': 50, 
        'level_obstacles': 3
    },
    {
        "obstacles": [], 
        "speed": 90, 
        'score_to_advance': 65, 
        'level_obstacles': 4
    },
]

SNAKE_SKINS = {
    'Classic': {
        'path': 'Graphics/Snake/Classic',
        'preview': pygame.image.load('Graphics/Snake/Previews/classic_preview.png')
    },
    'Neon': {
        'path': 'Graphics/Snake/Neon',
        'preview': pygame.image.load('Graphics/Snake/Previews/neon_preview.png')
    },
    # 'Pixel': {
    #     'path': 'Graphics/Snake/Pixel',
    #     'preview': pygame.image.load('Graphics/Snake/Previews/pixel_preview.png')
    # },
    'Green': {
        'path': 'Graphics/Snake/Green',
        'preview': pygame.image.load('Graphics/Snake/Previews/green_preview.png')
    },
}

# Paths to various game assets
BACKGROUND_IMAGE_PATH = 'Graphics/background_image.png'
BACKGROUND_VIDEO_PATH = 'Graphics/1087767644-preview.mp4'
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
APPLE_IMAGE_PATH = 'Graphics/apple.png'
CRUNCH_AUDIO_PATH = 'Audio/crunch.wav'
BG_MUSIC_PATH = 'Audio/Arcade.ogg'

# Color themes for the game
# Modify color theme definitions
CLASSIC_THEME = {
    'background': (137, 206, 148),      # Light green
    'board_light': (170, 215, 81),      # Light green
    'board_dark': (162, 209, 61),       # Dark green
    'font_color': (254, 215, 76),       # Yellow
    'info_color': (255, 255, 255),            # Black
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