# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Circular Fractal Tree Program.

Input:
- No input required from the user.

Output:
- Colorful Fractal Tree.

Features:
- Draws a circular fractal tree with colorful branches.
- Allows customization of the background pattern or texture.
- Plays background music using pygame mixer.
- Saves the turtle graphics window as an image file.

"""

import turtle as tu
from PIL import ImageGrab
import pygame
import pygetwindow as gw

def draw_branch(length: float, color: str, a: int, b: int, depth: int) -> None:
    """
    Draw a branch of the fractal tree with a given length and color, 
    recursively creating sub-branches.
    
    Args:
    - length (float): Length of the current branch.
    - color (str): Color of the branch.
    - a (int): Parameter 'a' for branch length adjustment.
    - b (int): Parameter 'b' for branch length adjustment.
    - depth (int): Depth of the current branch in the recursive tree.
    
    Returns:
    - None
    """
    if length < 10:
        return
    else:
        # Adjust the pen size based on the depth of the branch
        pensize = max(1, 10-depth)  
        roo.pensize(pensize)

        # Draw the actual branch and recursively create sub-branches
        roo.pencolor(color)
        roo.forward(length)
        roo.left(30)
        draw_branch(a * length / b, color, a, b, depth+1)
        roo.right(60)
        draw_branch(a * length / b, color, a, b, depth+1)
        roo.left(30)
        roo.pensize(pensize)
        roo.backward(length)

def play_background_music():
    """
    Play background music using pygame mixer.
    
    Returns:
    - None
    """
    pygame.mixer.init()
    pygame.mixer.music.load("../assets/audio/fractal_tree_bgmusic.mp3")  # Replace with your music file
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)  # -1 for infinite loop

def stop_background_music():
    """
    Stop background music.
    
    Returns:
    - None
    """
    pygame.mixer.music.stop()

def draw_background_pattern():
    """
    Draw a simple background pattern.
    
    Returns:
    - None
    """
    roo.speed(90000)  # Set the speed of drawing
    roo.pensize(1)
    roo.pencolor("gray")

    for _ in range(36):
        roo.circle(150)
        roo.right(10)

def draw_custom_background():
    """
    Draw a custom background pattern or texture.

    Returns:
    - None
    """
    roo.speed(90000)  # Set the speed of drawing
    roo.pensize(2)
    roo.pencolor("lightgray")

    # Draw a grid pattern
    for _ in range(10):
        roo.forward(300)
        roo.backward(300)
        roo.left(36)

    for _ in range(10):
        roo.forward(300)
        roo.backward(300)
        roo.left(36)
        roo.penup()
        roo.goto(roo.xcor(), roo.ycor() + 30)
        roo.pendown()

def save_as_image(file_path: str) -> None:
    """
    Save the turtle graphics window as an image file.
    
    Args:
    - file_path (str): File path for saving the image.
    
    Returns:
    - None
    """
    # Get the turtle graphics window by title
    windpw_title = "Fractal Tree Program"
    window = gw.getWindowsWithTitle(windpw_title)[0]

    # Get the bounding box of the turtle window
    x, y, width, height = window.left, window.top, window.width, window.height

    # Capture the screen and save it as an image
    image = ImageGrab.grab(bbox=(x, y, x+width, y+height))
    image.save(file_path)

if __name__ == '__main__':
    # Initialize the turtle and screen
    roo = tu.Turtle()
    wn = tu.Screen()
    
    # Set background color and title for the window
    wn.bgcolor("black")
    wn.title("Fractal Tree Program")

    # Play background music
    play_background_music()

    # Draw the background pattern
    draw_background_pattern()
    
    roo.left(90)  # Set initial orientation of the turtle
    roo.speed(90000)  # Set the speed of drawing
    
    # Define colors and lengths for the fractal tree branches
    colors = [['yellow', 'magenta', 'red', 'white'],
              ['lightgreen', 'red', 'yellow', 'white'],
              ['cyan', 'yellow', 'magenta', 'white']]
    lengths = [20, 40, 60]
    a = 2  # Initial value for the 'a' parameter
    
    # Loop through the lengths and corresponding color lists
    for length, color_list in zip(lengths, colors):
        a += 1
        for index, color in enumerate(color_list):
            draw_branch(length, color, a, a + 1, 5) # Start with depth 0
            
            # Adjust the orientation based on the color index
            if index % 2 == 0:
                roo.right(90)
                roo.speed(90000)
            elif index % 2 == 1 and color != 'white':
                roo.left(270)
                roo.speed(90000)
            elif color == 'white' and index % 2 == 1:
                continue  # Skip drawing when the color is white

    stop_background_music()  # Stop the background music
    
    # Save the fractal tree as an image
    save_as_image("fractal_tree.png")
    
    # Wait for a click to close the window
    wn.exitonclick()