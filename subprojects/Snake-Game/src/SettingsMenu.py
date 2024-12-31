"""
Settings Menu Class

Features:
- Display and handle the settings menu for the game
- Allow the player to adjust settings such as volume and color theme
- Provide options for changing control schemes and returning to the main menu

Methods:
- __init__(self, display_surface, main_instance): Constructor to initialize the SettingsMenu object
- update_color_theme(self): Update the colors based on the selected theme
- draw(self): Draw the settings menu on the display surface
- handle_color_theme(self, mouse_pos): Handle color theme cycling on click
- handle_control_scheme(self, mouse_pos): Handle control scheme cycling on click
- cycle_color_theme(self, direction): Cycle through color themes
- cycle_control_scheme(self, direction): Cycle through control schemes
- handle_events(self): Handle events such as mouse clicks and key presses
- run(self): Run the settings menu loop

"""

from Settings import *

class SettingsMenu:
    def __init__(self, display_surface, main_instance) -> None:
        logging.info("Initializing SettingsMenu object")

        try:
            pygame.font.init()
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            # Handle the error as needed, e.g., display an error message or exit the program.
            pygame.quit()
            exit()

        self.main_instance = main_instance

        # Set up fonts and icons
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()

        try:
            self.menu_font = pygame.font.Font(FONT_PATH, 40)
            self.title_font = pygame.font.Font(FONT_PATH, 80)
        except pygame.error as e:
            print(f"Error loading fonts: {e}")
            # Handle the error as needed, e.g., display an error message or exit the program.
            pygame.quit()
            exit()

        self.bg_music = main_instance.bg_music
        self.crunch_sound = main_instance.crunch_sound

        self.home_icon_surf = pygame.image.load(HOME_ICON_PATH)
        self.home_icon_rect = self.home_icon_surf.get_rect(topleft=(20, 25))

        self.help_icon_surf = pygame.image.load(HELP_ICON_PATH)
        self.help_icon_rect = self.help_icon_surf.get_rect(topright=(WINDOW_WIDTH - 20, 25))

        self.x_icon_surf = pygame.image.load(EXIT_ICON_PATH)
        self.x_icon_rect = self.x_icon_surf.get_rect(topright=(WINDOW_WIDTH - 20, 25))
        
        # Color themes and initial theme selection
        self.color_themes = {
            'Classic': CLASSIC_THEME,
            'Dark Mode': DARK_MODE_THEME,
            'Vibrant': VIBRANT_THEME,
            'Violet Blue': VIOLET_BLUE_THEME,
            'Vintage': VINTAGE_THEME,
        }
        self.selected_theme = 'Classic'

        # Set initial colors based on the selected theme
        self.background_color = self.color_themes[self.selected_theme]['background']

        # Set up UI elements
        self.bg_volume_slider = pygame.Rect(220, 300, 200, 50)
        self.crunch_vol_slider = pygame.Rect(220, 520, 200, 50)
        self.back_button = pygame.Rect(520, 650, 200, 50)

        # Set initial volume values
        self.bg_volume_value = 50
        self.crunch_vol_value = 50
        self.mute = False

        # Set up arrow buttons for cycling color themes
        self.left_arrow_rect = pygame.Rect(750, 310, 40, 40)
        self.right_arrow_rect = pygame.Rect(1050, 310, 40, 40)

        # Set up arrow buttons for cycling control schemes
        self.left_scheme_arrow_rect = pygame.Rect(750, 530, 40, 40)
        self.right_scheme_arrow_rect = pygame.Rect(1050, 530, 40, 40)

        # Control schemes and initial scheme selection
        self.control_schemes = {
            'Arrow Keys': ARROW_KEYS,
            'WASD': WASD_KEYS,
            'IJKL': IJKL_KEYS,
        }
        self.selected_control_scheme = 'Arrow Keys'

        # Snake skins and initial skin selection
        self.preview_rect = pygame.Rect(800, 470, 240, 120)
        self.snake_skins = SNAKE_SKINS
        self.selected_skin = 'Classic'

        # Add skin selection arrows
        self.left_skin_arrow_rect = pygame.Rect(750, 420, 40, 40)
        self.right_skin_arrow_rect = pygame.Rect(1050, 420, 40, 40)

    def draw_sliders(self):
        # Draw curved borders for sliders
        pygame.draw.rect(self.display_surface, (160, 234, 222), self.bg_volume_slider, border_radius=20)
        pygame.draw.rect(self.display_surface, (160, 234, 222), self.crunch_vol_slider, border_radius=20)

        # Draw sliders
        pygame.draw.rect(self.display_surface, (0, 141, 213), self.bg_volume_slider, border_radius=20, width=3)
        pygame.draw.rect(self.display_surface, (0, 141, 213), self.crunch_vol_slider, border_radius=20, width=3)
        
        # Draw text labels
        self.display_surface.blit(self.bg_volume_text, (150, 230))
        self.display_surface.blit(self.crunch_vol_text, (180, 450))

        # Draw slider handles with a gradient color
        bg_handle_x = int(self.bg_volume_slider.left + self.bg_volume_value * self.bg_volume_slider.width / 100)
        bg_handle_x = max(self.bg_volume_slider.left + 15, min(self.bg_volume_slider.right - 30, bg_handle_x))
        pygame.draw.circle(self.display_surface, (37, 110, 255), (bg_handle_x, self.bg_volume_slider.centery), 15)

        crunch_handle_x = int(self.crunch_vol_slider.left + self.crunch_vol_value * self.crunch_vol_slider.width / 100)
        crunch_handle_x = max(self.crunch_vol_slider.left + 15, min(self.crunch_vol_slider.right - 30, crunch_handle_x))
        pygame.draw.circle(self.display_surface, (37, 110, 255), (crunch_handle_x, self.crunch_vol_slider.centery), 15)

    def draw(self):
        logging.info("Drawing SettingsMenu")

        settings_background_image = pygame.image.load(SETTINGS_BACKGROUND_IMAGE_PATH)
        settings_background_image_rect = settings_background_image.get_rect(topleft=(0, 0))

        # Render text for various elements
        self.title_text = self.title_font.render('Settings', True, (13, 12, 29))
        self.title_rect = self.title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))

        self.bg_volume_text = self.menu_font.render('Background Volume', True, (244, 71, 8))
        self.crunch_vol_text = self.menu_font.render('Crunch Volume', True, (244, 71, 8))
        self.back_text = self.menu_font.render('Back', True, (255, 255, 255))
        
        self.color_theme_text = self.menu_font.render('Color Theme', True, (244, 71, 8))
        self.color_theme_rect = pygame.Rect(550, 300, 200, 50)

        self.control_scheme_text = self.menu_font.render('Control Scheme', True, (244, 71, 8))
        self.control_scheme_rect = pygame.Rect(520, 350, 200, 50)

        # Clear the display
        self.display_surface.blit(settings_background_image, settings_background_image_rect)
        self.display_surface.blit(self.title_text, self.title_rect)

        # Draw volume sliders
        self.draw_sliders()
        
        # Draw color theme section
        self.display_surface.blit(self.color_theme_text, (800, 230))
        theme_names = list(self.color_themes.keys())
        current_index = theme_names.index(self.selected_theme)
        current_theme_name = theme_names[current_index]
        theme_text = self.menu_font.render(current_theme_name, True, (0, 141, 213))
        theme_rect = pygame.Rect(800, 300, 240, 60)
        pygame.draw.rect(self.display_surface, (68, 229, 231), theme_rect, border_radius=20, width=3)
        pygame.draw.rect(self.display_surface, (160, 234, 222), theme_rect, border_radius=20)
        self.display_surface.blit(theme_text, (theme_rect.centerx - theme_text.get_width() // 2, theme_rect.centery - theme_text.get_height() // 2))

        # Draw arrow buttons for cycling color themes
        pygame.draw.polygon(self.display_surface, (0, 141, 213), [(self.left_arrow_rect.centerx - 8, self.left_arrow_rect.centery),
                                                                   (self.left_arrow_rect.centerx + 8, self.left_arrow_rect.centery - 8),
                                                                   (self.left_arrow_rect.centerx + 8, self.left_arrow_rect.centery + 8)])
        
        pygame.draw.polygon(self.display_surface, (0, 141, 213), [(self.right_arrow_rect.centerx + 8, self.right_arrow_rect.centery),
                                                                   (self.right_arrow_rect.centerx - 8, self.right_arrow_rect.centery - 8),
                                                                   (self.right_arrow_rect.centerx - 8, self.right_arrow_rect.centery + 8)])
        
        self.display_surface.blit(self.control_scheme_text, (770, 450))

        # Draw control scheme section
        self.display_surface.blit(self.control_scheme_text, (770, 450))
        scheme_names = list(self.control_schemes.keys())
        current_index = scheme_names.index(self.selected_control_scheme)
        current_scheme_name = scheme_names[current_index]
        scheme_text = self.menu_font.render(current_scheme_name, True, (0, 141, 213))
        scheme_rect = pygame.Rect(800, 520, 240, 60)
        pygame.draw.rect(self.display_surface, (68, 229, 231), scheme_rect, border_radius=20, width=3)
        pygame.draw.rect(self.display_surface, (160, 234, 222), scheme_rect, border_radius=20)
        self.display_surface.blit(scheme_text, (scheme_rect.centerx - scheme_text.get_width() // 2, scheme_rect.centery - scheme_text.get_height() // 2))

        # Draw arrow buttons for cycling control schemes
        pygame.draw.polygon(self.display_surface, (0, 141, 213), [(self.left_scheme_arrow_rect.centerx - 8, self.left_scheme_arrow_rect.centery),
                                                                    (self.left_scheme_arrow_rect.centerx + 8, self.left_scheme_arrow_rect.centery - 8),
                                                                    (self.left_scheme_arrow_rect.centerx + 8, self.left_scheme_arrow_rect.centery + 8)])
        
        pygame.draw.polygon(self.display_surface, (0, 141, 213), [(self.right_scheme_arrow_rect.centerx + 8, self.right_scheme_arrow_rect.centery),
                                                                    (self.right_scheme_arrow_rect.centerx - 8, self.right_scheme_arrow_rect.centery - 8),
                                                                    (self.right_scheme_arrow_rect.centerx - 8, self.right_scheme_arrow_rect.centery + 8)])

        # Draw back button
        pygame.draw.ellipse(self.display_surface, (222, 26, 26), self.back_button)
        self.display_surface.blit(self.back_text, (self.back_button.centerx - self.back_text.get_width() // 2, self.back_button.centery - self.back_text.get_height() // 2))

        # Draw home icon
        self.display_surface.blit(self.home_icon_surf, self.home_icon_rect)

        # Draw help icon
        self.display_surface.blit(self.help_icon_surf, self.help_icon_rect)

        # Draw snake skin selection
        self.snake_skin_text = self.menu_font.render('Snake Skin', True, (244, 71, 8))
        self.display_surface.blit(self.snake_skin_text, (800, 350))

        # Draw skin selector
        skin_rect = pygame.Rect(800, 410, 240, 60)
        pygame.draw.rect(self.display_surface, (68, 229, 231), skin_rect, border_radius=20, width=3)
        pygame.draw.rect(self.display_surface, (160, 234, 222), skin_rect, border_radius=20)

        skin_text = self.menu_font.render(self.selected_skin, True, (0, 141, 213))
        self.display_surface.blit(skin_text, (skin_rect.centerx - skin_text.get_width() // 2, 
                                              skin_rect.centery - skin_text.get_height() // 2))
        
        # Draw skin preview
        preview_image = self.snake_skins[self.selected_skin]['preview']
        # Scale preview image to fit the preview rect while maintaining aspect ratio
        preview_width = self.preview_rect.width
        preview_height = self.preview_rect.height
        scaled_preview = pygame.transform.scale(preview_image, (preview_width, preview_height))

        # Draw preview background
        pygame.draw.rect(self.display_surface, (160, 234, 222), self.preview_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, (68, 229, 231), self.preview_rect, border_radius=10, width=3)

        # Draw preview image
        perview_pos = (self.preview_rect.centerx - preview_width // 2, 
                       self.preview_rect.centery - preview_height // 2)
        self.display_surface.blit(scaled_preview, perview_pos)
        
        # Draw skin selection arrows
        pygame.draw.polygon(self.display_surface, (0, 141, 213), 
            [(self.left_skin_arrow_rect.centerx - 8, self.left_skin_arrow_rect.centery),
             (self.left_skin_arrow_rect.centerx + 8, self.left_skin_arrow_rect.centery - 8),
             (self.left_skin_arrow_rect.centerx + 8, self.left_skin_arrow_rect.centery + 8)])
        
        pygame.draw.polygon(self.display_surface, (0, 141, 213), 
            [(self.right_skin_arrow_rect.centerx + 8, self.right_skin_arrow_rect.centery),
             (self.right_skin_arrow_rect.centerx - 8, self.right_skin_arrow_rect.centery - 8),
             (self.right_skin_arrow_rect.centerx - 8, self.right_skin_arrow_rect.centery + 8)])

        # Update the display
        pygame.display.flip()

    def handle_color_theme(self, mouse_pos):
        logging.info("Handling color theme in SettingsMenu")

        # Handle color theme cycling on click
        if self.color_theme_rect.collidepoint(mouse_pos):
            theme_names = list(self.color_themes.keys())
            current_index = theme_names.index(self.selected_theme)
            next_index = (current_index + 1) % len(theme_names)
            self.selected_theme = theme_names[next_index]

    def handle_control_scheme(self, mouse_pos):
        logging.info("Handling control scheme in SettingsMenu")

        # Handle control scheme cycling on click
        if self.control_scheme_rect.collidepoint(mouse_pos):
            scheme_names = list(self.control_schemes.keys())
            current_index = scheme_names.index(self.selected_control_scheme)
            next_index = (current_index + 1) % len(scheme_names)
            self.selected_control_scheme = scheme_names[next_index]

    def cycle_color_theme(self, direction):
        logging.info("Cycling color theme in SettingsMenu")

        # Cycle through color themes
        theme_names = list(self.color_themes.keys())
        current_index = theme_names.index(self.selected_theme)
        next_index = (current_index + direction) % len(theme_names)
        self.selected_theme = theme_names[next_index]

    def cycle_control_scheme(self, direction):
        logging.info("Cycling control scheme in SettingsMenu")

        # Cycle through control schemes
        scheme_names = list(self.control_schemes.keys())
        current_index = scheme_names.index(self.selected_control_scheme)
        next_index = (current_index + direction) % len(scheme_names)
        self.selected_control_scheme = scheme_names[next_index]

    def cycle_snake_skin(self, direction):
        logging.info("Cycling snake skin in SettingsMenu")

        # Cycle through snake skins
        skin_names = list(self.snake_skins.keys())
        current_index = skin_names.index(self.selected_skin)
        next_index = (current_index + direction) % len(skin_names)
        self.selected_skin = skin_names[next_index]
        self.main_instance.snake.update_skin(self.snake_skins[self.selected_skin]['path'])

    def display_help(self):
        logging.info("Displaying help message in SettingsMenu")
        
        # Help instructions for the settings menu
        instructions = {
            "Settings menu"   : ":    'SHIFT' + 'S'",
            "Quit Game"       : ":    'ALT' + 'Q'",
            "Help Message"    : ":    'SHIFT' + 'H'",
            "Start Game"      : ":    'SPACE'",
            "Exit Settings"   : ":    'ESC'",
            "Exit Help"       : ":    'ESC'",
            "Pause Game"      : ":    'P'",
            "Restart Game"    : ":    'R'",
            "Mute/Unmute"     : ":    'M'",
        }

        help_data = [
            {
                "heading": "Objective",
                "content": [
                    "Eat Apples & grow the snake",
                    "Avoid Walls or Snake's body",
                    "Aim for Highest score"
                ]
            },
            {
                "heading": "Controls",
                "content": [
                    "Arrow keys - move Snake",
                    "Sliders - adjust Volume levels",
                    "Back button - back to Main Menu",
                    "Home icon - back to Start Screen",
                    "Help icon - view Help Message"
                ]
            }
        ]

        # Font for help instructions
        help_font = pygame.font.Font(FONT_PATH, 25)
        help_heading_font = pygame.font.Font(FONT_PATH, 40)
        shortcut_font = pygame.font.Font(FONT_PATH, 30)

        # Clear the display
        self.help_bg_image = pygame.image.load(HELP_BACKGROUND_IMAGE_PATH)
        self.help_bg_image_rect = self.help_bg_image.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.help_bg_image, self.help_bg_image_rect)

        # Render and blit each line of the help instructions
        help_heading_text = help_heading_font.render("SlitherQuest - Help", True, (250, 166, 19))
        help_heading_rect = help_heading_text.get_rect(center=(WINDOW_WIDTH // 2, 170))
        self.display_surface.blit(help_heading_text, help_heading_rect)

        # Calculate text positions
        shortcut_text_x = WINDOW_HEIGHT // 2 - 155
        shortcut_text_y = 315
        shortcut_line_ht = 37
        help_data_x = WINDOW_HEIGHT // 2 + 240
        help_data_y = 260
        help_data_line_ht = 35

        sortcut_text = shortcut_font.render("Shortcut", True, (161, 7, 2))
        sortcut_rect = sortcut_text.get_rect(topleft=(shortcut_text_x, 260))
        self.display_surface.blit(sortcut_text, sortcut_rect)

        line_text = shortcut_font.render("-------------------------", True, (161, 7, 2))
        line_rect = line_text.get_rect(topleft=(shortcut_text_x, 285))
        self.display_surface.blit(line_text, line_rect)

        for action, shortcut in instructions.items():
            action_text = help_font.render(action, True, (2, 8, 135))
            action_rect = action_text.get_rect(topleft=(shortcut_text_x, shortcut_text_y))
            self.display_surface.blit(action_text, action_rect)

            shortcut_text = help_font.render(shortcut, True, (2, 8, 135))
            shortcut_rect = shortcut_text.get_rect(topleft=(shortcut_text_x + 190, shortcut_text_y))  # Adjust the x position
            self.display_surface.blit(shortcut_text, shortcut_rect)

            shortcut_text_y += shortcut_line_ht

        for section in help_data:
            heading_text = shortcut_font.render(section['heading'], True, (161, 7, 2))
            heading_rect = heading_text.get_rect(topleft=(help_data_x, help_data_y))
            self.display_surface.blit(heading_text, heading_rect)
            line_text = shortcut_font.render("-------------------------", True, (161, 7, 2))
            line_rect = line_text.get_rect(topleft=(help_data_x, help_data_y + 25))
            self.display_surface.blit(line_text, line_rect)

            help_data_y += help_data_line_ht

            for content_line in section['content']:
                content_text = help_font.render(content_line, True, (2, 8, 135))
                content_rect = content_text.get_rect(topleft=(help_data_x, help_data_y + 15))
                self.display_surface.blit(content_text, content_rect)
                help_data_y += help_data_line_ht
        
            help_data_y += help_data_line_ht // 2

        footer_font = pygame.font.Font(FONT_PATH, 40)
        footer_text = footer_font.render("Enjoy the game!", True, (43, 151, 32))
        footer_text_rect = footer_text.get_rect(bottomright=(WINDOW_WIDTH // 2 + 160, WINDOW_HEIGHT - 150))
        self.display_surface.blit(footer_text, footer_text_rect)

        self.display_surface.blit(self.x_icon_surf, self.x_icon_rect)

        # Update the display
        pygame.display.flip()

        # Wait for user input to exit help (e.g., click on 'X' icon)
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == MOUSEBUTTONDOWN:
                    if self.x_icon_rect.collidepoint(pygame.mouse.get_pos()):
                        waiting_for_input = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    waiting_for_input = False

    def update_color_theme(self):
        logging.info("Updating color theme in SettingsMenu")

        # Update colors based on the selected theme
        self.background_color = self.color_themes[self.selected_theme]['background']

    def update_volume(self):
        # Update slider positions based on volume values
        if self.mute == True:
            self.bg_volume_value = 0.0
            self.crunch_vol_value = 0.0
            self.draw_sliders()
        elif self.mute == False:
            self.bg_volume_value = 50
            self.crunch_vol_value = 50
            self.draw_sliders()

    def handle_events(self):
        logging.info("Handling events in SettingsMenu")

        # Update color theme before handling events
        self.update_color_theme()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN: 
                if event.mod & KMOD_ALT and event.key == K_q:
                    pygame.quit()
                    exit()

                elif event.key == K_ESCAPE:
                    return True
            
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    # Cycle color theme with arrow keys
                    self.cycle_color_theme(1 if event.key == K_RIGHT else -1)
                
                elif event.key == K_UP or event.key == K_DOWN:
                    # Cycle control scheme with arrow keys
                    self.cycle_control_scheme(1 if event.key == K_DOWN else -1)

                elif event.mod & KMOD_SHIFT and event.key == K_h:
                    self.display_help()

                elif event.key == K_m:
                    if self.mute == False:
                        self.mute = True
                        pygame.mixer.Sound.set_volume(self.bg_music, 0.0)
                        pygame.mixer.Sound.set_volume(self.crunch_sound, 0.0)
                        self.update_volume()
                    elif self.mute == True:
                        self.mute = False
                        pygame.mixer.Sound.set_volume(self.bg_music, 1.0)
                        pygame.mixer.Sound.set_volume(self.crunch_sound, 1.0)
                        self.update_volume()
                
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check for slider adjustments and button clicks
                if self.bg_volume_slider.collidepoint(mouse_pos):
                    self.bg_volume_value = (mouse_pos[0] - self.bg_volume_slider.left) / self.bg_volume_slider.width * 100
                    self.bg_volume_value = max(0, min(100, self.bg_volume_value))

                elif self.crunch_vol_slider.collidepoint(mouse_pos):
                    self.crunch_vol_value = (mouse_pos[0] - self.crunch_vol_slider.left) / self.crunch_vol_slider.width * 100
                    self.crunch_vol_value = max(1, min(100, self.crunch_vol_value))

                elif self.back_button.collidepoint(mouse_pos):
                    return True
                
                elif self.left_arrow_rect.collidepoint(mouse_pos):
                    self.cycle_color_theme(-1)

                elif self.right_arrow_rect.collidepoint(mouse_pos):
                    self.cycle_color_theme(1)
                
                elif self.left_scheme_arrow_rect.collidepoint(mouse_pos):
                    self.cycle_control_scheme(-1)
                
                elif self.right_scheme_arrow_rect.collidepoint(mouse_pos):
                    self.cycle_control_scheme(1)

                elif self.home_icon_rect.collidepoint(mouse_pos):
                    self.main_instance.start_screen()
                    return True
                
                elif self.help_icon_rect.collidepoint(mouse_pos):
                    self.display_help()
                
                elif self.left_skin_arrow_rect.collidepoint(mouse_pos):
                    self.cycle_snake_skin(-1)
                
                elif self.right_skin_arrow_rect.collidepoint(mouse_pos):
                    self.cycle_snake_skin(1)
                
                # Check for color theme and control scheme changes
                self.handle_color_theme(mouse_pos)
                self.handle_control_scheme(mouse_pos)

        return False

    def run(self):
        logging.info("Running SettingsMenu")

        while True:
            try:
                if self.handle_events():
                    break
                
                # Draw the settings menu
                self.draw()
                self.clock.tick(FPS)
            except pygame.error as e:
                print(f"Pygame error in SettingsMenu: {e}")
                pygame.quit()
                exit()
            except Exception as e:
                print(f"Error in SettingsMenu: {e}")
                pygame.quit()
                exit()
