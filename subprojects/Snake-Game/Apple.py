"""
Apple Class

Features:
- Set the position of the Apple on the game board
- Draw the Apple on the game board
- Add a pulsating effect to the Apple size using the sin function

Methods:
- __init__(self, snake, obstacles): Constructor to initialize the Apple object
- set_pos(self): Set the position for the Apple
- draw(self): Draw the Apple on the game board

"""

from Settings import *
from math import sin

class Apple:
    def __init__(self, snake, obstacles):
        logging.info("Initializing Apple object")

        # Initialize Apple position, display surface, Snake reference, and obstacle list
        self.pos = pygame.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.snake = snake
        self.obstacles = obstacles

        # Initialize the rectangle to be used for drawing the scaled apple
        self.scaled_rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)

        # Set the initial position for the Apple
        self.set_pos()

        try:
            # Try loading the apple image
            self.surf = pygame.image.load(join('Graphics', 'apple.png')).convert_alpha()
        except pygame.error as e:
            print(f"Error loading apple image: {e}")
            # Handle the error as needed, e.g., display an error message or use a default image.
            # In this case, we'll use a placeholder image for simplicity.
            self.surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.surf.fill((255, 0, 0))  # Red placeholder color

        # Initialize the scaled surface for drawing with the initial position
        self.scaled_surf = self.surf.copy()

    def set_pos(self):
        logging.info("Setting position for Apple")

        # Keep generating a new position until a valid one is found
        while True:
            new_pos = (random.randint(0, COLS - 1), random.randint(1, ROWS - 1))
            if new_pos not in self.snake.body and new_pos not in self.obstacles:
                self.pos = pygame.Vector2(new_pos)
                self.scaled_rect.topleft = (int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE))
                return

    def draw(self):
        logging.info("Drawing Apple")

        try:
            # Ensure the Apple is not placed at the top row (y == 0)
            while self.pos.y == 0:
                self.set_pos()

            # Add a pulsating effect to the Apple size using the sin function
            scale = 1 + sin(pygame.time.get_ticks() / 600) / 3

            # Scale the original surface to create the pulsating effect
            self.scaled_surf = pygame.transform.smoothscale(self.surf, (int(self.surf.get_width() * scale), int(self.surf.get_height() * scale)))

            # Set the rectangle for drawing at the scaled position
            self.scaled_rect = self.scaled_surf.get_rect(
                center=(int(self.pos.x * CELL_SIZE + CELL_SIZE / 2), int(self.pos.y * CELL_SIZE + CELL_SIZE / 2)))

            # Draw the scaled Apple on the display surface
            self.display_surface.blit(self.scaled_surf, self.scaled_rect)

        except pygame.error as e:
            print(f"Error drawing apple: {e}")
            # Handle the error as needed, e.g., display an error message or exit the program.
