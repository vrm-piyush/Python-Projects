"""
Password Generator Program.

Input:
- User interaction to specify password length, character sets, and the number of passwords.
- Optional choice to save passwords to a file and hash passwords before saving.

Output:
- Generated passwords, strength indicator, entropy, and optionally saved to a file.

Features:
- Allows the user to specify the length of the password, choose character sets (lowercase, uppercase, numbers, symbols), and determine the number of passwords to generate.
- Checks for common security policies, such as a minimum length of 8 characters and the inclusion of at least one uppercase letter, number, or symbol.
- Generates multiple passwords based on user preferences.
- Displays generated passwords and copies each password to the clipboard with an option to copy the next password.
- Provides a strength indicator (out of 4) and entropy (in bits) for each generated password.
- Offers the option to save generated passwords to a file, with the ability to append to an existing file.
- Optionally hashes passwords before saving, allowing users to choose the hashing algorithm.
- Handles input validation and provides appropriate error messages.

"""

import random, pyperclip, hashlib, math, os

def generate_password(pass_len, use_uppercase=True, use_numbers=True, use_symbols=True):
    """Generate a random password based on user-specified criteria."""
    characters = ""

    # Customize character set based on user preferences
    characters += "abcdefghijklmnopqrstuvwxyz"
    if use_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        characters += "0123456789"
    if use_symbols:
        characters += "!@#$%^&*()_+-=[]\\{}|;':\",./<>?"

    # Check if at least one character set is selected
    if not characters:
        print("Error: At least one character set (lowercase, uppercase, numbers, symbols) must be selected.")
        return None

    # Generate a password by selecting 'pass_len' number of random characters from the defined set.
    password = "".join(random.choice(characters) for _ in range(pass_len))
    
    return password

def password_strength_indicator(password):
    """Calculate the strength of a password based on the presence of different character types."""
    strength = 0

    # Check for the presence of different character types
    if any(char.islower() for char in password):
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if any(char in "!@#$%^&*()_+-=[]\\{}|;':\",./<>?" for char in password):
        strength += 1

    return strength

def calculate_entropy(password):
    """Calculate the entropy of a password."""
    # Calculate entropy using the formula: log2(number of possible combinations)
    num_possible_combinations = sum(1 for char in set(password))
    entropy = math.log2(num_possible_combinations) * len(password)
    return entropy

def save_to_file(filename, passwords, hashed_passwords=None, append=False):
    """Save passwords (and optionally hashed passwords) to a file."""
    mode = 'a' if append else 'w'
    with open(filename, mode) as file:
        if hashed_passwords:
            for password, hashed_password in zip(passwords, hashed_passwords):
                file.write(f"Original: {password}, Hashed: {hashed_password}\n")
        else:
            for password in passwords:
                file.write(f"Original: {password}\n")
    print(f"Passwords {'appended to' if append else 'saved to'} {filename}")


def copy_to_clipboard(password):
    """Copy a password to the clipboard for easy access."""
    pyperclip.copy(password)
    print(f"Password copied to clipboard: {password}")

def hash_password(password, algorithm='sha256'):
    """Hash a password using the specified algorithm."""
    hasher = hashlib.new(algorithm)
    hasher.update(password.encode('utf-8'))
    hashed_password = hasher.hexdigest()
    return hashed_password

if __name__ == '__main__':
    try:
        # Prompt the user to enter the desired length of the password and convert it to an integer.
        pass_len = int(input('Enter the length of the password: '))

        # Allow users to customize character sets
        use_uppercase = input('Include Uppercase Letters? (y/n): ').lower() == 'y'
        use_numbers = input('Include Numbers? (y/n): ').lower() == 'y'
        use_symbols = input('Include Symbols? (y/n): ').lower() == 'y'

        # Check password policy compliance
        if pass_len < 8 or not (use_uppercase or use_numbers or use_symbols):
            print("Password does not meet common security policies. Please consider a longer length and include uppercase letters, numbers, or symbols.")
            exit()

        # Prompt the user for the number of passwords to generate
        num_passwords = int(input('Enter the number of passwords to generate: '))

        # Generate multiple passwords
        passwords = [generate_password(pass_len, use_uppercase, use_numbers, use_symbols) for _ in range(num_passwords)]

        # Display and save passwords
        print("\nGenerated Passwords:")
        for idx, password in enumerate(passwords, start=1):
            print(f"{idx}. {password}")
            copy_to_clipboard(password)
            input("Press Enter to copy the next password...")

        # Strength Indicator and entropy for each password
        print("\nPassword Strength and Entropy:")
        for idx, password in enumerate(passwords, start=1):
            strength = password_strength_indicator(password)
            entropy = calculate_entropy(password)
            print(f"{idx}. Strength: {strength}/4, Entropy: {entropy:.2f} bits")

        # Copy the first password to clipboard
        copy_to_clipboard(passwords[0])

        # Ask if the user wants to save passwords to a file
        save_to_file_option = input("\nDo you want to save these passwords to a file? (y/n): ").lower()
        if save_to_file_option == 'y':
            filename = input('Enter the filename to save passwords (e.g., passwords.txt): ')
            
            # Check if the file already exists
            file_exists = os.path.isfile(filename)

            # Ask if the user wants to append to the existing file
            if file_exists:
                append_option = input("The file already exists. Do you want to append to it? (y/n): ").lower()
                append_to_file = append_option == 'y'
            else:
                append_to_file = False

            # Ask if the user wants to hash the passwords
            hash_password_option = input("\nDo you want to hash these passwords before saving? (y/n): ").lower()
            if hash_password_option == 'y':
                hash_algorithm = input('Enter the hashing algorithm (e.g., sha256): ')
                hashed_passwords = [hash_password(password, hash_algorithm) for password in passwords]
                save_to_file(filename, passwords, hashed_passwords, append=append_to_file)
            else:
                save_to_file(filename, passwords, append=append_to_file)

    except ValueError:
        print("Error: Please enter valid input.")
    except Exception as e:
        print(f"An error occurred: {e}")