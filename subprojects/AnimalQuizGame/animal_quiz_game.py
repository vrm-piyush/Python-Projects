# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Animal Quiz Game Program.

Input:
- Number of questions the user wants to attempt: 5 or 10.
- User's selection of categories.
- User's choice of difficulty level.

Output:
- User's score based on the number of correct guesses.

Features:
- Users can select categories (Mammals, Birds, Reptiles, Fish, Insects).
- Users can choose difficulty levels (easy, medium, hard).
- Visuals (images) are displayed for each question.
- Users have a time limit (10 seconds) to answer each question.
- Users receive feedback on correct or incorrect answers.
- The final score is displayed based on the number of correct guesses.

"""

import random
from PIL import Image
import threading
import os

def check_guess(guess, answer, score):
    """
    Check if the user's guess matches the correct answer.
    
    Args:
    - guess (str): The user's guess.
    - answer (str): The correct answer.
    - score (int): The current score of the user.
    
    Returns:
    - int: Updated score after checking the guess.
    """
    still_guessing = True
    attempt = 0

    while still_guessing and attempt < 3:
        if guess.lower() == answer.lower():
            print("Correct Answer!")
            score += 1
            still_guessing = False
        else:
            if attempt < 2:
                guess = input("Sorry! Wrong Answer!! Try again: ")
            attempt += 1
    
    if attempt == 3:
        print(f"The correct answer is {answer}")
    
    return score

def display_visual(visual_path):
    """
    Display visuals (images or sounds) related to the quiz question.
    
    Args:
    - visual_path (str): The file path of the visual (image or sound).
    """
    # For images, you can use the Pillow library (PIL).
    img = Image.open(visual_path)
    img.show()

    # For sounds, you might use a library like pygame to play the sound.
    # Example: pygame.mixer.Sound(visual_path).play()

def quiz_game(num_questions, selected_categories, difficulty_level):
    """
    Conduct the Animal Quiz game based on the number of questions, selected categories, and difficulty level.

    Args:
    - num_questions (int): Number of questions to present in the quiz.
    - selected_categories (list): List of categories chosen by the user.
    - difficulty_level (str): Difficulty level chosen by the user ('easy', 'medium', 'hard').
    """

    print(f"Animal Quiz - {num_questions} Questions ({difficulty_level} difficulty)")
    score = 0

    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the 'Images' folder path
    images_folder = os.path.join(script_dir, 'Images')

    quiz = {
        'Mammals': {
            'easy': {'Which bear lives at the North Pole? ': ('Polar Bear', os.path.join(images_folder, 'polar_bear_image.jpg')), 'Which animal is known as the "ship of the desert"? ': ('Camel', os.path.join(images_folder, 'camel_image.jpg'))},
            'medium': {'What is the largest big cat in the world? ': ('Siberian Tiger', os.path.join(images_folder, 'tiger_image.jpg')), 'Which is the fastest land animal? ': ('Cheetah', os.path.join(images_folder, 'cheetah_image.jpg'))},
            'hard': {'What is the only mammal capable of sustained flight? ': ('Bat', os.path.join(images_folder, 'bat_image.jpg')),},
        },
        'Birds': {
            'easy': {'Which bird is known for its ability to mimic human speech? ': ('Parrot', os.path.join(images_folder, 'parrot_image.jpg'))},
            'medium': {'Which bird is known for its long migration journey, often flying thousands of miles between breeding and wintering grounds? ': ('Arctic Tern', os.path.join(images_folder, 'arctic_tern_image.jpg'))},
            'hard': {'Which bird is known as the "king of the birds" and can mimic a variety of sounds? ': ('Lyrebird', os.path.join(images_folder, 'lyrebird_image.jpg')),},
        },
        'Reptiles': {
            'easy': {'Which animal is known for its ability to change color to match its surroundings? ': ('Chameleon', os.path.join(images_folder, 'chameleon_image.jpg')),},
            'medium': {'What is the only marsupial that lives in North America? ': ('Opossum', os.path.join(images_folder, 'opossum_image.jpg'))},
            'hard': {'What is the largest species of lizard? ': ('Komodo Dragon', os.path.join(images_folder, 'komodo_dragon_image.jpg'))},
        },
        'Fish': {
            'easy': {'Which fish is known for its ability to inflate itself when threatened? ': ('Pufferfish', os.path.join(images_folder, 'pufferfish_image.jpg'))},
            'medium': {'Which fish is the fastest swimmer in the ocean? ': ('Sailfish', os.path.join(images_folder, 'sailfish_image.jpg'))},
            'hard': {'What is the largest species of shark? ': ('Whale Shark', os.path.join(images_folder, 'whale_shark_image.jpg'))},
        },
        'Insects': {
            'easy': {'Which insect is known for its bioluminescence? ': ('Firefly', os.path.join(images_folder, 'firefly_image.jpg'))},
            'medium': {'Which insect undergoes complete metamorphosis? ': ('Butterfly', os.path.join(images_folder, 'butterfly_image.jpg'))},
            'hard': {'Which insect is the largest in the world? ': ('Giant Weta', os.path.join(images_folder, 'giant_weta_image.jpg'))},
        },
    }

    selected_quiz = {}
    for category in selected_categories:
        if category in quiz:
            selected_quiz.update(quiz[category][difficulty_level])

    # Check if the number of specified questions is greater than the available questions.
    num_questions = min(num_questions, len(selected_quiz))

    # Check if there are questions available for the selected categories and difficulty level.
    if not selected_quiz:
        print("No questions available for the selected categories and difficulty level.")
    else:
        # Randomly select 'num_questions' questions from the selected_quiz dictionary.
        selected_quiz = dict(random.sample(list(selected_quiz.items()), num_questions))

    for quest, (ans, visual_path) in selected_quiz.items():
        print(quest)
        display_visual(visual_path)
        user_input = None

        def get_user_input():
            nonlocal user_input
            user_input = input("Your answer: ")

        # Set a timer thread for each question
        timer_thread = threading.Thread(target=get_user_input)
        timer_thread.start()

        # Wait for a certain time (e.g., 10 seconds) and then check the answer
        timer_thread.join(10)

        # Check if the user provided an answer
        if user_input is not None:
            score = check_guess(user_input, ans, score)
        else:
            print("Time's up! No answer provided.")

    print(f"Your Score is: {score}/{num_questions}")

if __name__ == '__main__':
    print("Welcome to the Animal Quiz Game!")

    # Define available categories and difficulty levels
    categories = ['Mammals', 'Birds', 'Reptiles', 'Fish', 'Insects']
    difficulty_levels = ['easy', 'medium', 'hard']

    # Prompt the user to select categories
    selected_categories = []
    while True:
        print("Available Categories: ", categories)
        selected_category = input("Choose a category (or type 'done' to start the quiz):  ").capitalize()

        if selected_category == 'Done':
            break

        if selected_category in categories:
            selected_categories.append(selected_category)
            
        else:
            print("Invalid category. Please choose from the available categories.")

    difficulty_level = None
    while difficulty_level not in difficulty_levels:
        difficulty_level = input("Choose difficulty level (easy, medium, hard): ").lower()

    # Prompt the user to enter the number of questions they want to attempt.
    while True:
        try:
            num_questions = int(input("Enter the number of questions you want to attempt (5 or 10): "))
            if num_questions not in [5, 10]:
                raise ValueError("Please enter either 5 or 10.")
            break
        except ValueError as e:
            print(e)

    # Start the quiz game with the specified number of questions and selected categories.
    quiz_game(num_questions, selected_categories, difficulty_level)