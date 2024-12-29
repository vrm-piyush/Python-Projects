# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Snake Game Program.

Input:
- Arrow keys to change direction.
- Space to start the game.
- P to pause and resume the game.
- R to play again after game over.
- Q to quit the game.

Output:
- Start screen with game title and instructions.
- Snake game window.
- Game over screen with high score.
- Settings menu for volume and color settings.

Features:
- Levels with increasing difficulty.
- Pause and resume functionality.
- Responsive controls for smooth movement.
- Obstacles to navigate around.
- Animations for snake growth and level transitions.
- Sound effects for in-game events.
- Randomized apple effects.
- Persistent scoreboard for high scores.
- Customizable settings menu.
- Engaging game over screen with high score display.

Note: To control volume, press 'LShift' or 'RShift' to open the settings menu.

Dependencies:
- Pygame library for game development.

Ensure the required audio files and images are in the specified paths.

"""

import pygame
from Settings import *
from Snake import Snake
from Apple import Apple
from SettingsMenu import SettingsMenu

# Main class for the Snake game
class Main:
    def __init__(self):
        logging.info("Initializing Main object")

        # Initialize the Pygame library and set up the game window
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake')

        # Set up background rectangles for drawing the game board
        self.bg_rects = [pygame.Rect((col + int(row % 2 == 0)) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                         for col in range(0, COLS, 2) for row in range(1,ROWS)]
        
        # Load icons and set up the update event
        self.home_icon_surf = pygame.image.load(HOME_ICON_PATH)
        self.home_icon_rect = self.home_icon_surf.get_rect(topleft=(15, 20))
        self.resume_pause_icon_surf = pygame.image.load(PAUSE_ICON_PATH)
        self.resume_pause_icon_rect = self.resume_pause_icon_surf.get_rect(topright=(WINDOW_WIDTH - 225, 10))
        self.help_icon_surf = pygame.image.load(HELP_ICON_PATH)
        self.help_icon_rect = self.help_icon_surf.get_rect(topright=(WINDOW_WIDTH - 160, 20))
        self.settings_icon_surf = pygame.image.load(SETTINGS_ICON_PATH)
        self.settings_icon_rect = self.settings_icon_surf.get_rect(topright=(WINDOW_WIDTH - 90, 20))
        self.close_icon_surf = pygame.image.load(X_ICON_PATH)
        self.close_icon_rect = self.close_icon_surf.get_rect(topright=(WINDOW_WIDTH - 20, 20))

        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)

        # Set initial game state and load fonts and sounds
        self.game_active = False
        self.paused = False
        self.game_over_displayed = False
        self.crunch_sound = pygame.mixer.Sound(join('Audio', 'crunch.wav'))
        self.bg_music = pygame.mixer.Sound(join('Audio', 'Arcade.ogg'))
        self.bg_music.set_volume(0.5)
        # self.bg_music.play(-1)

        # Set up fonts for the game
        self.pause_font = pygame.font.Font(FONT_PATH, 100)
        self.pause_text = self.pause_font.render('Paused', True, (56, 74, 12))
        self.pause_info_font = pygame.font.Font(FONT_PATH, 25)
        self.pause_info_text = self.pause_info_font.render('Click the button or Press \'P\' to Resume ', True, (56, 74, 12))
        self.resume_btn_icon_surf = pygame.image.load(RESUME_BTN_ICON_PATH)
        self.resume_btn_icon_rect = self.resume_btn_icon_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
        self.game_font = pygame.font.Font(FONT_PATH, 25)

        # Set up level progression data and obstacles
        self.level = 1
        self.levels_data = [
            {"obstacles": [], "speed": 250, 'score_to_advance': 5, 'level_obstacles': 0},
            {"obstacles": [], "speed": 200, 'score_to_advance': 10, 'level_obstacles': 2},
            {"obstacles": [], "speed": 150, 'score_to_advance': 15, 'level_obstacles': 3},
            {"obstacles": [], "speed": 100, 'score_to_advance': 20, 'level_obstacles': 4},
            {"obstacles": [], "speed": 75, 'score_to_advance': 25, 'level_obstacles': 5},
        ]

        # Load obstacle image
        self.obstacle_image = pygame.image.load(OBSTACLE_IMAGE_PATH).convert_alpha()

        # Place obstacles for each level
        for level_data in self.levels_data[1:]:
            level_data["obstacles"] = [(random.randint(0, COLS - 1), random.randint(0, ROWS - 1)) for _ in range(level_data["level_obstacles"])]

        self.obstacles = self.levels_data[self.level - 1]["obstacles"]
        self.level_speed = self.levels_data[self.level - 1]["speed"]
        pygame.time.set_timer(self.update_event, self.level_speed)

        # Create instances of Snake, Apple, and SettingsMenu
        self.snake = Snake()
        self.apple = Apple(self.snake, self.obstacles)
        self.settings_menu = SettingsMenu(self.display_surface, self)

        # Set up color and control settings from the settings menu
        self.background_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['background']
        self.board_light_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['board_light']
        self.board_dark_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['board_dark']
        self.font_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['font_color']
        self.info_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['info_color']

        self.up_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['up']
        self.down_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['down']
        self.left_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['left']
        self.right_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['right']

        # Load all high scores from file
        self.load_high_scores()
        self.save_high_scores()

        # Display the start screen
        self.start_screen()

    # Load high scores from file
    def load_high_scores(self):
        logging.info("Loading high scores")

        try:
            with open('high_scores.txt', 'r') as file:
                self.high_scores = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            self.high_scores = []

    # Save high scores to file
    def save_high_scores(self):
        logging.info("Saving high scores")

        with open('high_scores.txt', 'w') as file:
            for score in self.high_scores:
                file.write(f'{score}\n')
    
    # Update high scores list
    def update_high_scores(self):
        logging.info("Updating high scores")

        current_score = len(self.snake.body) - START_LENGTH
        self.high_scores.append(current_score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:1]
        self.save_high_scores()

    # Draw home icon on the game board
    def draw_home_icon(self) -> None:
        self.display_surface.blit(self.home_icon_surf, self.home_icon_rect)

    # Draw settings icon on the game board
    def draw_settings_icon(self) -> None:
        self.display_surface.blit(self.settings_icon_surf, self.settings_icon_rect)

    # Draw help icon on the game board
    def draw_help_icon(self) -> None:
        self.display_surface.blit(self.help_icon_surf, self.help_icon_rect)

    # Draw close icon on the game board
    def draw_close_icon(self) -> None:
        self.display_surface.blit(self.close_icon_surf, self.close_icon_rect)

    # Place an obstacle on the game board
    def place_obstacle(self) -> None:
        logging.info("Placing obstacle")

        # Keep generating a new position until a valid one is found
        while True:
            obstacle_pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))           
            if (
                obstacle_pos not in self.snake.body and
                obstacle_pos != self.apple.pos and
                obstacle_pos not in self.obstacles and
                obstacle_pos[0] != 0 and obstacle_pos[1] != 0
            ):
                self.obstacles.append(obstacle_pos)
                return 

    # Draw obstacles on the game board
    def draw_obstacles(self) -> None:
        logging.info("Drawing obstacles")

        # Draw the obstacles on the game board
        for obstacle in self.obstacles:
            obstacle_pixel_pos = (obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE)
            obstacle_rect = pygame.Rect(obstacle_pixel_pos[0], obstacle_pixel_pos[1], CELL_SIZE, CELL_SIZE)
            self.display_surface.blit(self.obstacle_image, obstacle_rect.topleft)

    # Draw the shadow effect on the game board
    def draw_shadow(self) -> None:
        logging.info("Drawing shadow")

        shadow_surf = pygame.Surface(self.display_surface.get_size())
        shadow_surf.fill((0, 255, 0))
        shadow_surf.set_colorkey((0, 255, 0))
        
        # Draw the shadow effect for the snake and apple
        shadow_surf.blit(self.apple.scaled_surf, self.apple.scaled_rect.topleft + SHADOW_SIZE)
        for surf, rect in self.snake.draw_data:
            shadow_surf.blit(surf, rect.topleft + SHADOW_SIZE)

        # Invert the shadow mask and set the opacity
        mask = pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf = mask.to_surface()
        shadow_surf.set_colorkey((255, 255, 255))
        shadow_surf.set_alpha(SHADOW_OPACITY)

        self.display_surface.blit(shadow_surf, (0, 0))

    # Draw the game board background
    def draw_bg(self) -> None:
        logging.info("Drawing background")

        self.display_surface.fill(self.board_light_color)
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, self.board_dark_color, rect)

        # Draw the game board background
        bar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, CELL_SIZE)
        pygame.draw.rect(self.display_surface, (46, 49, 56), bar_rect)
        pygame.draw.rect(self.display_surface,(224, 225, 221), bar_rect, width=2)

        # Draw the home and settings icons
        self.draw_home_icon()
        self.display_surface.blit(self.resume_pause_icon_surf, self.resume_pause_icon_rect)
        self.draw_settings_icon()
        self.draw_help_icon()
        self.draw_close_icon()

        # Draw the obstacles
        self.draw_obstacles()

        # Render and blit the level
        level_font = pygame.font.Font(FONT_PATH, 35)
        level_text = f'Level: {self.level}'
        level_surf = level_font.render(level_text, True, (244, 157, 55))
        level_rect = level_surf.get_rect(center=(WINDOW_WIDTH // 2 + 20, CELL_SIZE // 2))
        self.display_surface.blit(level_surf, level_rect)

        # Render and blit the top score text surface
        info_font = pygame.font.Font(FONT_PATH, 25)
        top_score_text = f'High Score: {self.high_scores[0] if self.high_scores else 0}'
        top_score_surf = info_font.render(top_score_text, True, (0, 204, 255))
        top_score_rect = top_score_surf.get_rect(midleft=(CELL_SIZE + 70, CELL_SIZE // 2))
        self.display_surface.blit(top_score_surf, top_score_rect)

  # Draw the score on the game board
    def draw_score(self) -> None:
        logging.info("Drawing score")

        # Render and blit the score text surface
        score_text = str(len(self.snake.body) - START_LENGTH)
        score_surf = self.game_font.render(score_text, True, (56, 74, 12))

        score_x = int(CELL_SIZE * COLS - score_surf.get_width() - 50)
        score_y = int(CELL_SIZE * ROWS - score_surf.get_height() - 30)

        score_rect = score_surf.get_rect(center=(score_x, score_y))
        apple_rect = self.apple.surf.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height + 6)
        
        pygame.draw.rect(self.display_surface, self.board_light_color, bg_rect)
        self.display_surface.blit(score_surf, score_rect)
        self.display_surface.blit(self.apple.surf, apple_rect)
        pygame.draw.rect(self.display_surface, (56, 74, 12), bg_rect, 2)

    # Display the pause screen
    def draw_pause_screen(self):
        logging.info("Displaying pause screen")

        # Set up the overlay and pause screen text surfaces
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT * CELL_SIZE))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, CELL_SIZE))

        # Blit the pause screen text surfaces
        pause_rect = self.pause_text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT + CELL_SIZE) // 2 - 100))
        pause_info_rect = self.pause_info_text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT + CELL_SIZE) // 2 + 200))
        self.display_surface.blit(self.pause_text, pause_rect)
        self.display_surface.blit(self.resume_btn_icon_surf, self.resume_btn_icon_rect)
        self.display_surface.blit(self.pause_info_text, pause_info_rect)

        pygame.display.update()

    # Handle input for changing the snake's direction
    def input(self) -> None:
        logging.info("Handling input")

        keys = pygame.key.get_pressed()
        # Change the snake's direction based on the arrow keys
        if keys[self.right_key]:
            self.snake.direction = pygame.Vector2(1, 0) if self.snake.direction.x != -1 else self.snake.direction
        if keys[self.left_key]:
            self.snake.direction = pygame.Vector2(-1, 0) if self.snake.direction.x != 1 else self.snake.direction
        if keys[self.up_key]:
            self.snake.direction = pygame.Vector2(0, -1) if self.snake.direction.y != 1 else self.snake.direction
        if keys[self.down_key]:
            self.snake.direction = pygame.Vector2(0, 1) if self.snake.direction.y != -1 else self.snake.direction
                
    # Handle collision with the apple, obstacles, and game boundaries
    def collision(self) -> None:
        logging.info("Handling collision")

        # Check for collision with the apple
        if self.snake.body[0] == self.apple.pos:
            self.snake.has_eaten = True
            self.apple.set_pos()
            self.crunch_sound.play()

        # Check for collision with the obstacles
        if self.snake.body[0][1] < 0:
            self.game_active = False
            self.game_over_screen()
        
        # Check for collision with the snake's body or game boundaries
        if self.snake.body[0] in self.snake.body[1:] or not (0 <= self.snake.body[0].x < COLS and 1 <= self.snake.body[0].y < ROWS) or self.snake.body[0] in self.obstacles:
            self.game_active = False
            self.game_over_screen()

    # Reset the game level
    def reset_level(self) -> None:
        logging.info("Resetting level")

        # Reset the game level to the initial state
        self.level = 1
        self.obstacles = []
        for _ in range(self.levels_data[self.level - 1]["level_obstacles"]):
            self.place_obstacle()
        self.level_speed = self.levels_data[self.level - 1]["speed"]
        pygame.time.set_timer(self.update_event, self.level_speed)
        
    # Display the start screen
    def start_screen(self) -> bool:
        logging.info("Displaying start screen")

        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        background_image_rect = background_image.get_rect()

        # Set up fonts for the start screen
        start_font = pygame.font.Font(FONT_PATH, 70)
        press_space_font = pygame.font.Font(FONT_PATH, 25)

        center_y = WINDOW_HEIGHT // 2

        # Render the start screen text surfaces
        title_surf = start_font.render('Snake Game', True, self.font_color)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, center_y - 150))

        play_icon_surf = pygame.image.load(PLAY_ICON_PATH)
        play_icon_rect = play_icon_surf.get_rect(center=(WINDOW_WIDTH // 2, center_y + 30))

        press_space_surf = press_space_font.render('Click Play Button or Press Space to Start Game', True, self.info_color)
        press_space_rect = press_space_surf.get_rect(center=(WINDOW_WIDTH // 2, center_y + 180))

        # Display the start screen and handle events
        clock = pygame.time.Clock()
        animation_time = 0
        animation_speed = 2500

        while True:
            self.update_settings()
            self.display_surface.blit(background_image, background_image_rect)
            
            # Handle events for the start screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:         # Quit the game
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN: 
                    if event.mod & KMOD_ALT and event.key == K_q:           # Quit the game
                        pygame.quit()
                        exit()

                    elif event.key == K_SPACE:                              # Start the game
                        return True
                
                    elif event.mod & KMOD_SHIFT and event.key == K_s:       # Open settings menu
                        self.settings_menu.run()
                        self.update_volume()
                    
                    elif event.mod & KMOD_SHIFT and event.key == K_h:
                        self.settings_menu.display_help()

                    elif event.key == K_m:
                        pygame.mixer.Sound.set_volume(self.bg_music, 0)
                        pygame.mixer.Sound.set_volume(self.crunch_sound, 0)
                    
                    elif event.key == K_n:
                        self.update_volume()

                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if play_icon_rect.collidepoint(mouse_pos):
                        return True

                    if self.settings_icon_rect.collidepoint(mouse_pos):     # Open settings menu
                        self.settings_menu.run()
                        self.update_volume()
                        self.update_settings()
                    
                    if self.help_icon_rect.collidepoint(mouse_pos):         # Display help screen
                        self.settings_menu.display_help()

                    if self.close_icon_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()

            # Animate the start screen text surfaces
            if animation_time < animation_speed:
                alpha = int(255 * (animation_time / animation_speed))
                title_surf.set_alpha(alpha)
                play_icon_surf.set_alpha(alpha)
                press_space_surf.set_alpha(alpha)
                background_image.set_alpha(alpha)
            else:
                title_surf.set_alpha(255)
                play_icon_surf.set_alpha(255)
                press_space_surf.set_alpha(255)
                background_image.set_alpha(255)
    
            # Blit the start screen text surfaces
            self.display_surface.blit(title_surf, title_rect)
            self.display_surface.blit(play_icon_surf, play_icon_rect)
            self.display_surface.blit(press_space_surf, press_space_rect)
            self.draw_settings_icon()
            self.draw_help_icon()
            self.draw_close_icon()
            
            pygame.display.update()                     # Update the display
            clock.tick(FPS)                             # Set the frame rate
            animation_time += clock.get_rawtime()       # Update the animation time

    # Display the game over screen
    def game_over_screen(self):
        logging.info("Displaying game over screen")

        # Set up fonts for the game over screen
        game_over_font = pygame.font.Font(FONT_PATH, 70)
        score_font = pygame.font.Font(FONT_PATH, 30)
        info_font = pygame.font.Font(FONT_PATH, 20)

        # Render and blit the game over screen text surfaces
        game_over_text = game_over_font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

        score_text = f'Your Score: {len(self.snake.body) - START_LENGTH}'
        score_text_rendered = score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_text_rendered.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

        info_text = 'Press R to play again or Q to quit.'
        info_text_rendered = info_font.render(info_text, True, (255, 255, 255))
        info_rect = info_text_rendered.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))

        # Blit the game over screen text surfaces
        self.display_surface.blit(game_over_text, game_over_rect)
        self.display_surface.blit(score_text_rendered, score_rect)
        self.display_surface.blit(info_text_rendered, info_rect)

        while True:
            for event in pygame.event.get():                # Handle events for the game over screen
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:                 # Handle key presses 
                    if event.key == K_r:                    # Restart the game
                        self.snake.reset()
                        self.game_active = True
                        self.reset_level()
                        self.game_over_displayed = False    
                        return
                    elif event.key == K_q:                  # Quit the game
                        pygame.quit()
                        exit()
            
            pygame.display.update()
            self.update_high_scores()

    # Update the volume settings
    def update_volume(self):
        logging.info("Updating volume settings")

        # Update the volume settings for the game
        bg_volume = self.settings_menu.bg_volume_value / 100
        crunch_volume = self.settings_menu.crunch_vol_value / 100
        pygame.mixer.Sound.set_volume(self.crunch_sound, crunch_volume)
        pygame.mixer.Sound.set_volume(self.bg_music, bg_volume)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_m]:
            pygame.mixer.Sound.set_volume(self.bg_music, 0)
            pygame.mixer.Sound.set_volume(self.crunch_sound, 0)
            self.settings_menu.bg_volume_value = 0
            self.settings_menu.crunch_vol_value = 0
        elif keys[pygame.K_n]:
            pygame.mixer.Sound.set_volume(self.bg_music, bg_volume)
            pygame.mixer.Sound.set_volume(self.crunch_sound, crunch_volume)
            self.settings_menu.bg_volume_value = bg_volume * 100
            self.settings_menu.crunch_vol_value = crunch_volume * 100

    # Update the game settings
    def update_settings(self):
        # Update the color settings
        self.background_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['background']
        self.board_light_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['board_light']
        self.board_dark_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['board_dark']
        self.font_color = self.settings_menu.color_themes[self.settings_menu.selected_theme]['font_color']

        # Update the control settings
        self.up_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['up']
        self.down_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['down']
        self.left_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['left']
        self.right_key = self.settings_menu.control_schemes[self.settings_menu.selected_control_scheme]['right']

        self.render_text_surfaces()

    # Render the text surfaces for the game
    def render_text_surfaces(self):
        logging.info("Rendering text surfaces")

        # Set up fonts for the game
        start_font = pygame.font.Font(FONT_PATH, 70)
        press_space_font = pygame.font.Font(FONT_PATH, 25)

        self.title_surf = start_font.render('Snake Game', True, self.font_color)
        self.title_rect = self.title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

        self.press_space_surf = press_space_font.render('Press Space to start game', True, self.info_color)
        self.press_space_rect = self.press_space_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    # Run the game
    def run(self):
        logging.info("Running game")

        self.update_volume()
        self.update_settings()

        try:
            # Main game loop
            while True:
                for event in pygame.event.get():                                                    # Handle events for the game
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == self.update_event:                                             # Update the game state
                        if self.game_active:
                            self.snake.update()
                            self.collision()

                    if event.type == KEYDOWN:
                        if event.mod & KMOD_ALT and event.key == K_q:
                            pygame.quit()
                            exit()

                        elif (event.key in [self.up_key, self.down_key, self.left_key, self.right_key]):     # Change the snake's direction
                            if  not self.game_active:
                                self.game_active = True

                        elif event.key == K_p:                                                               # Pause and resume the game
                            self.paused = not self.paused
                            if self.paused:
                                self.draw_pause_screen()
                                pygame.time.set_timer(self.update_event, 0)
                            else:
                                pygame.time.set_timer(self.update_event, self.level_speed)

                        elif (event.mod & KMOD_SHIFT) and event.key == K_s:                                  # Open settings menu
                            self.settings_menu.run()
                            self.update_volume()  
                            self.update_settings()   

                        elif event.key == K_m:
                            pygame.mixer.Sound.set_volume(self.bg_music, 0)
                            pygame.mixer.Sound.set_volume(self.crunch_sound, 0)
                        elif event.key == K_n:
                            self.update_volume() 

                    elif event.type == MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if self.home_icon_rect.collidepoint(mouse_pos):                                      # Return to start screen
                            self.start_screen() 

                        if self.resume_pause_icon_rect.collidepoint(mouse_pos):                                 # Pause and resume the game
                            self.paused = not self.paused
                            if self.paused:
                                self.draw_pause_screen()
                                pygame.time.set_timer(self.update_event, 0)
                            else:
                                pygame.time.set_timer(self.update_event, self.level_speed)                                

                        if self.settings_icon_rect.collidepoint(mouse_pos):                         # Open settings menu
                            self.settings_menu.run()
                            self.update_volume()
                            self.update_settings()    

                        if self.help_icon_rect.collidepoint(mouse_pos):                             # Display help screen
                            self.settings_menu.display_help()   

                        if self.close_icon_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            exit()

                        if self.paused:
                            # Check if the mouse click is on the resume button
                            if self.resume_btn_icon_rect.collidepoint(mouse_pos):
                                self.paused = False
                                pygame.time.set_timer(self.update_event, self.level_speed)
                            
                if not self.paused:
                    # Update the game state
                    if not self.game_over_displayed:
                        self.draw_bg()
                        self.snake.draw()
                        self.apple.draw()
                        self.draw_shadow()
                        self.input()
                        self.draw_score()

                        pygame.display.update()
                        pygame.time.Clock().tick(FPS)

                        # Check for level progression
                        if self.game_active and not self.game_over_displayed:
                            if len(self.snake.body) - START_LENGTH >= self.levels_data[self.level - 1]["score_to_advance"]:                 # Level up
                                self.level += 1
                                if self.level <= len(self.levels_data):
                                    self.obstacles = self.levels_data[self.level - 1]["obstacles"]
                                    self.level_speed = self.levels_data[self.level - 1]["speed"]
                                    pygame.time.set_timer(self.update_event, self.level_speed)
                                    self.snake_has_eaten = False
                                    self.update_settings()

                                elif len(self.snake.body) - START_LENGTH >= sum(level["score_to_advance"] for level in self.levels_data):   # All levels completed
                                    # All levels completed, continue until collision
                                    self.snake_has_eaten = False

                                else:                                                                                                       # Game over
                                    self.collision()
                                    if not self.game_active:
                                        self.game_over_screen()

                else:                                                                                                                       # Pause the game
                    pygame.time.Clock().tick(FPS)

        # Handle exceptions
        except Exception as e:
            logging.info(f"An unexpected error occurred: {str(e)}")

            error_message = f"An unexpected error occurred: {str(e)}"
            error_font = pygame.font.Font(FONT_PATH, 30)
            error_surf = error_font.render(error_message, True, (255, 0, 0))
            error_rect = error_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.display_surface.blit(error_surf, error_rect)

            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            exit()

if __name__ == '__main__':
    logging.info("Starting game")

    main = Main()
    main.run()