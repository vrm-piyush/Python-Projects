"""
Snake class

Features:
- Move the Snake on the game board
- Draw the Snake on the game board
- Update the Snake's body segments based on the direction of movement
- Handle the Snake's collision with itself, the game board boundaries, and obstacles

Methods:
- __init__(self): Constructor to initialize the Snake object
- import_surfs(self): Import the surfaces for the Snake graphics
- update(self): Update the Snake's position and body segments
- reset(self): Reset the Snake to its initial state
- update_head(self): Update the head segment of the Snake
- update_tail(self): Update the tail segment of the Snake
- update_body(self): Update the body segments of the Snake
- draw(self): Draw the Snake on the game board

"""

from Settings import *
from os import walk
from os.path import join

class Snake:
    def __init__(self):
        logging.info("Initializing Snake object")

        # Setup
        self.display_surface = pygame.display.get_surface()
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)]
        self.direction = pygame.Vector2(0, 0)
        self.has_eaten = False

        # Graphics
        self.surfs = self.import_surfs()
        self.draw_data = []
        self.head_surf = self.surfs['head_right']
        self.tail_surf = self.surfs['tail_left']
        self.update_body()

    def import_surfs(self):
        logging.info("Importing surfaces for Snake")

        surf_dict = {}
        try:
            # Load snake graphics from the specified folder
            for folder_path, _, image_names in walk(join('Graphics', 'Snake')):
                for image_name in image_names:
                    full_path = join(folder_path, image_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    surf_dict[image_name.split('.')[0]] = surface
        except FileNotFoundError as fe:
            print(f"Error loading images: {fe}")
            pygame.quit()
            exit()
        except pygame.error as pe:
            print(f"Pygame error: {pe}")
            pygame.quit()
            exit()
        except Exception as e:
            print(f"Error: {e}")
            pygame.quit()
            exit()

        return surf_dict

    def update_head(self):
        logging.info("Updating head of Snake")

        # Determine the head direction and update the head surface accordingly
        head_relation = self.body[1] - self.body[0]

        if head_relation == pygame.Vector2(-1, 0):
            self.head_surf = self.surfs['head_right']
        elif head_relation == pygame.Vector2(1, 0):
            self.head_surf = self.surfs['head_left']
        elif head_relation == pygame.Vector2(0, -1):
            self.head_surf = self.surfs['head_down']
        elif head_relation == pygame.Vector2(0, 1):
            self.head_surf = self.surfs['head_up']

    def update_tail(self):
        logging.info("Updating tail of Snake")

        # Determine the tail direction and update the tail surface accordingly
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == pygame.Vector2(1, 0):
            self.tail_surf = self.surfs['tail_left']
        elif tail_relation == pygame.Vector2(-1, 0):
            self.tail_surf = self.surfs['tail_right']
        elif tail_relation == pygame.Vector2(0, 1):
            self.tail_surf = self.surfs['tail_up']
        elif tail_relation == pygame.Vector2(0, -1):
            self.tail_surf = self.surfs['tail_down']

    def update_body(self):
        logging.info("Updating body of Snake")

        self.draw_data = []
        for index, block in enumerate(self.body):
            # Calculate the position of each body block
            x = block.x * CELL_SIZE
            y = block.y * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Determine the appropriate surface for each body block
            if index == 0:
                self.draw_data.append((self.head_surf, rect))
            elif index == len(self.body) - 1:
                self.draw_data.append((self.tail_surf, rect))
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                # Determine if the body block is a straight or corner segment
                if previous_block.x == next_block.x:
                    self.draw_data.append((self.surfs['body_vertical'], rect))
                elif previous_block.y == next_block.y:
                    self.draw_data.append((self.surfs['body_horizontal'], rect))
                else:  # corners
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        self.draw_data.append((self.surfs['body_tl'], rect))
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        self.draw_data.append((self.surfs['body_bl'], rect))
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        self.draw_data.append((self.surfs['body_tr'], rect))
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        self.draw_data.append((self.surfs['body_br'], rect))

    def update(self):
        logging.info("Updating Snake")

        if self.direction != pygame.Vector2(0, 0):                  # Ensure the snake only moves when there's a direction
            # Move the snake's body
            if not self.has_eaten:
                body_copy = self.body[:-1]
            else:
                body_copy = self.body[:]
                self.has_eaten = False

            # Calulate the new head position with wrapping logic
            new_head = self.body[0] + self.direction

            # Wrap horizontally (left and right boundaries)
            new_head.x %= COLS
            
            # Wrap vertically (top and bottom boundaries)
            if new_head.y < 1.0:                                # If the new head goes above the playable area
                new_head.y = ROWS                              # Wrap to the bottom of the screen
            elif new_head.y >= ROWS:                            # If the new head goes below the playable area
                new_head.y = 1                                  # Wrap to the top of the screen

            # Insert the new head
            body_copy.insert(0, new_head)
            self.body = body_copy[:]

            self.update_head()
            self.update_tail()
            self.update_body()

    def reset(self):
        logging.info("Resetting Snake")

        # Reset the snake to its initial state
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)]
        self.direction = pygame.Vector2(0, 0)

        self.update_head()
        self.update_tail()
        self.update_body()

    def draw(self):
        logging.info("Drawing Snake")

        # Draw each body block on the display surface
        for surf, rect in self.draw_data:
            self.display_surface.blit(surf, rect)
