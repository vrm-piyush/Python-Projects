# Password Generator

![password generator](image.png)

## Project Overview

The Password Generator is a Python program that enables users to generate random passwords based on their preferences. It allows users to specify the length of the password, choose character sets (lowercase, uppercase, numbers, symbols), and determine the number of passwords to generate. The program checks for common security policies, such as a minimum length of 8 characters and the inclusion of at least one uppercase letter, number, or symbol. It also provides a strength indicator, entropy calculation, and the option to copy passwords to the clipboard.

## Features

- **Password Customization:**

  - Users can specify the length of the password and choose character sets (lowercase, uppercase, numbers, symbols).

- **Security Policy Check:**

  - Checks for common security policies, including a minimum length of 8 characters and the inclusion of at least one uppercase letter, number, or symbol.

- **Multiple Password Generation:**

  - Generates multiple passwords based on user preferences.

- **Strength Indicator:**

  - Provides a strength indicator (out of 4) for each generated password based on the presence of different character types.

- **Entropy Calculation:**

  - Calculates the entropy (in bits) for each generated password.

- **Clipboard Copy:**

  - Copies each password to the clipboard with an option to copy the next password.

- **File Saving:**

  - Offers the option to save generated passwords to a file.

- **Password Hashing:**

  - Optionally hashes passwords before saving, allowing users to choose the hashing algorithm.

- **Input Validation:**
  - Handles input validation and provides appropriate error messages.

## How to Use

1. **Run the Program:**

   - Execute the program and follow the on-screen prompts.

2. **Specify Password Criteria:**

   - Enter the desired length of the password and choose character sets.

3. **Generated Passwords:**

   - View and copy generated passwords with strength indicators and entropy calculations.

4. **Save to File:**
   - Optionally, choose to save generated passwords to a file.

## Example

```bash
cd PasswordGenerator
python password_generator.py
```

```python
Enter the length of the password: 12
Include Uppercase Letters? (y/n): y
Include Numbers? (y/n): y
Include Symbols? (y/n): y
Enter the number of passwords to generate: 3

Generated Passwords:
1. aB3#eF6@hG8
   Press Enter to copy the next password...

2. xY2*pQ9!vR7
   Press Enter to copy the next password...

3. zZ4!tH1#oK5
   Press Enter to copy the next password...

Password Strength and Entropy:
1. Strength: 4/4, Entropy: 72.00 bits
2. Strength: 4/4, Entropy: 72.00 bits
3. Strength: 4/4, Entropy: 72.00 bits

Password copied to clipboard: aB3#eF6@hG8

Do you want to save these passwords to a file? (y/n): y
Enter the filename to save passwords (e.g., passwords.txt): generated_passwords.txt
The file already exists. Do you want to append to it? (y/n): n
Do you want to hash these passwords before saving? (y/n): y
Enter the hashing algorithm (e.g., sha256): sha256
Passwords saved to generated_passwords.txt
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vrm-piyush/PasswordGenerator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd PasswordGenerator
   ```

3. Run the program:

   ```bash
   python password_generator.py
   ```

## Features to be Added

- **Error Handling:**

  - Implement comprehensive error handling for various scenarios.

- **User-Friendly Interface:**

  - Enhance the user interface for a more engaging experience.

- **Password Sharing:**

  - Add the ability to share generated passwords securely.

- **More Hashing Algorithms:**

  - Include additional hashing algorithms for password hashing.

- **Improved Security Policies:**
  - Implement more advanced security policies for password generation.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/PasswordGenerator/issues) or submit a pull request.

---
