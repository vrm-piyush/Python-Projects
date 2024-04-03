"""
Generate Stories based on predefined lists.

Input:
- Lists of Strings containing different scenarios, characters, locations, etc.

Output:
- A randomly generated story combining elements from the lists.

Features:
- Allows the user to choose the type of story (scenario) they want to generate.
- Provides predefined lists for different scenarios such as mystery, adventure, romance, and fantasy.
- Dynamically fills in a story template with randomly chosen elements from the selected scenario's lists.
- Capitalizes the first letter of the story and adds a period at the end if missing.
- Gives the option to save the generated story to a file or share it on social media.
- Validates user choices and handles invalid inputs gracefully.
- Easily extensible by adding more scenarios and lists.

"""

import random

def generate_story(scenario_lists, chosen_scenario):
    """
    Generate a grammatically correct story using predefined lists.

    Args:
    - scenario_lists (dict): Dictionary containing lists for different scenarios.
    - chosen_scenario (str): Chosen scenario.

    Returns:
    - str: Grammatically correct story.
    """
    scenario = scenario_lists[chosen_scenario]
    story_template = "{when}, {who} named {name}, who lived in {residence}, went to the {went} and {happened}."
    
    # Fill in the details dynamically.
    story = story_template.format(
        when=random.choice(scenario['when']),
        who=random.choice(scenario['who']),
        name=random.choice(scenario['name']),
        residence=random.choice(scenario['residence']),
        went=random.choice(scenario['went']),
        happened=random.choice(scenario['happened'])
    )

    # Capitalize the first letter of the story and add a period at the end if missing.
    story = story.capitalize() + '.' if not story.endswith('.') else story

    return story

def save_story_to_file(story, chosen_scenario):
    """
    Save the generated story to a file.

    Args:
    - story (str): The story to be saved.
    - chosen_scenario (str): The chosen scenario for including in the filename.
    - filename (str): The name of the file.
    """
    # Construct the filename with the chosen scenario.
    filename_with_scenario = f"{chosen_scenario}"

    with open(filename_with_scenario, 'w') as file:
        file.write(story)
    print(f"Story saved to {filename_with_scenario}")

def get_user_choice(prompt, options):
    """
    Get user choice from the provided options.

    Args:
    - prompt (str): Prompt message.
    - options (list): List of available options.

    Returns:
    - str: User's choice.
    """
    while True:
        print(prompt)
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Invalid choice. Please enter a valid number.")


if __name__ == '__main__':
    # Define lists containing different scenarios, characters, names, residences, places, and events.
    scenarios = ['mystery', 'adventure', 'romance', 'fantasy']

    scenario_lists = {
        'mystery': {
            'when': ['A dark and stormy night', 'During a mysterious eclipse', 'In an abandoned mansion'],
            'who': ['a detective', 'a ghost', 'a secret agent', 'a mysterious stranger'],
            'name': ['Sherlock', 'Elena', 'Phoenix', 'Isabella'],
            'residence': ['an eerie castle', 'an old mansion', 'a haunted house', 'a secret hideout'],
            'went': ['crime scene', 'secret lair', 'dark alley', 'ancient library'],
            'happened': ['discovered a hidden clue', 'solved a cryptic riddle', 'encountered a ghost', 'unraveled a conspiracy']
        },
        'adventure': {
            'when': ['In a faraway land', 'On a quest for treasure', 'During an epic journey'],
            'who': ['an adventurer', 'a brave knight', 'a pirate', 'a treasure hunter'],
            'name': ['Archer', 'Luna', 'Captain Jack', 'Indiana'],
            'residence': ['a bustling city', 'a mysterious island', 'a hidden temple', 'a distant kingdom'],
            'went': ['treasure island', 'ancient ruins', 'enchanted forest', 'dragon\'s lair'],
            'happened': ['found a legendary artifact', 'defeated a mythical creature', 'discovered a hidden passage', 'escaped a trap']
        },
        'romance': {
            'when': ['Under the starry sky', 'During a romantic dinner', 'On a moonlit beach'],
            'who': ['a lover', 'a couple', 'a hopeless romantic', 'a charming stranger'],
            'name': ['Romeo', 'Juliet', 'Amelia', 'Oliver'],
            'residence': ['a cozy cottage', 'a beachfront villa', 'a city apartment', 'a countryside mansion'],
            'went': ['romantic dinner', 'stroll in the park', 'boat ride', 'dance under the stars'],
            'happened': ['expressed undying love', 'shared a passionate kiss', 'exchanged heartfelt vows', 'created everlasting memories']
        },
        'fantasy': {
            'when': ['In a magical realm', 'During a celestial alignment', 'In the land of mythical creatures'],
            'who': ['a wizard', 'an elf', 'a dragon rider', 'a sorceress'],
            'name': ['Merlin', 'Eowyn', 'Drakon', 'Seraphina'],
            'residence': ['an enchanted tower', 'a mystical forest', 'a floating island', 'a hidden valley'],
            'went': ['enchanted castle', 'dragon\'s lair', 'fairy fountain', 'celestial observatory'],
            'happened': ['unleashed powerful magic', 'befriended mythical creatures', 'discovered ancient artifacts', 'saved the realm from darkness']
        },
        # Add more scenarios and lists as needed.
    }

    # Get user's choice for the type of story.
    chosen_scenario = get_user_choice("Choose the type of story:", scenarios)

    # Generate a random story using the selected scenario's lists.
    story = generate_story(scenario_lists, chosen_scenario)

    # Display the randomly generated story to the user.
    print(f"\nHere is your {chosen_scenario} story:\n")
    print(story)

    # Ask the user if they want to save or share the story.
    save_or_share = input("\nDo you want to save this story to a file or share it on social media? (save/share/no): ").lower()

    if save_or_share == 'save':
        save_story_to_file(story, chosen_scenario)
    elif save_or_share == 'share':
        # Add code to share on social media (e.g., print a message or use social media API).
        print("Sharing on social media is not implemented in this example.")
    else:
        print("Okay, the story was not saved or shared.")