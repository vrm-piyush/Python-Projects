"""
Acronym Generator Program.

Input:
- String to convert to Acronym.

Output:
- Acronym of the input string.

Features:
- Allows the user to input a single phrase or multiple phrases separated by a delimiter.
- Provides options for specifying a delimiter, acronym separator, and casing (upper or lower).
- Generates and displays the acronym for each input phrase.
- Supports the option to continue generating acronyms for multiple phrases.

"""

import re

def create_acronym(phrase: str, separator: str = "", casing: str = "upper") -> str:
    """
    Generate an acronym from the given phrase by using the first letter of each word.

    Args:
    - phrase (str): The input phrase from which acronym needs to be generated.
    - separator (str): The separator between acronym letters (default is an empty string).
    - casing (str): The casing of the acronym ("upper" or "lower", default is "upper").

    Returns:
    - str: Acronym generated from the input phrase.
    """
    words = re.findall(r'\b\w', phrase)
    acronym = separator.join(words).upper() if casing == "upper" else separator.join(words).lower()
    return acronym

def validate_casing(casing: str) -> str:
    """
    Validate user input for casing.

    Args:
    - casing (str): The user-provided casing.

    Returns:
    - str: Validated casing ("upper" or "lower").
    """
    while casing.lower() not in ['upper', 'lower','']:
        print("Invalid casing. Please enter 'upper' or 'lower'.")
        casing = input("Enter acronym casing ('upper' or 'lower'): ")
    
    return casing.lower()

if __name__ == "__main__":
    try:
        while True: 
            phrases_input = input("Enter single or multiple phrases\n(Enter multiple phrases separated by a delimiter (e.g., comma)): ")
            delimiter = input("Enter the delimiter used to separate phrases (press Enter for default ','): ") or ','

            if delimiter:
                phrases = [phrase.strip() for phrase in phrases_input.split(delimiter)]
                is_single_phrase = False
            else:
                phrases = [phrases_input.strip()]
                is_single_phrase = True

            separator = input("Enter acronym separator (or press Enter for no separator): ")
            casing = input("Enter acronym casing ('upper' or 'lower'): ")
            casing = validate_casing(casing)

            for input_phrase in phrases:
                acronym_result = create_acronym(input_phrase, separator, casing)
                print(f"\nThe acronym for '{input_phrase}' is: {acronym_result}\n")

            if not is_single_phrase:
                continue_input = input("Do you want to continue (yes/no)? ").lower()
                if continue_input != "yes":
                    break

    except Exception as e:
        print(f"An error occurred: {e}")