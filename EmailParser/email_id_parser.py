"""
Separate the Username and Domain name from an Email ID.

Input:
- User Email ID

Output:
- Username and Domain name extracted from the Email ID.

Features:
- Validates the format of the input email ID using a simple regular expression.
- Normalizes the email address to lowercase.
- Extracts the username, subdomain, and main domain from the email ID.
- Handles cases where the domain may have subdomains.

"""

import re

def extract_username_and_domain(email_id: str) -> tuple:
    """
    Extract username and domain name from the given email ID.

    Args:
    - email_id (str): The input email ID.

    Returns:
    - tuple: Extracted username and domain name.
    """
    # Validate email format using a simple regular expression.
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not email_regex.match(email_id):
        raise ValueError("Invalid email format.")

    # Normalize email address to lowercase.
    email_id = email_id.lower()

    # Extract the username and domain.
    username, domain = email_id.split("@", 1)

    # Split domain into subdomain and main domain.
    domain_parts = domain.split(".")
    
    if len(domain_parts) > 2:
        subdomain = domain_parts[0]
        main_domain = ".".join(domain_parts[1:])
    elif len(domain_parts) == 2:
        subdomain = None
        main_domain = ".".join(domain_parts)
    else:
        raise ValueError("Invalid domain format.")


    return username, subdomain, main_domain

if __name__ == '__main__':
    try:
        while True:
            # Prompt the user to enter their email ID and strip any leading/trailing whitespaces.
            email_id = input("Enter your Email ID: ").strip()

            # Extract username and domain from the email ID.
            username, subdomain, main_domain = extract_username_and_domain(email_id)

            # Display the extracted information to the user.
            print(f"Username: {username}")
            print(f"Subdomain: {subdomain}" if subdomain else "No subdomain")
            print(f"Main Domain: {main_domain}")

            continue_input = input("Do you want to continue (yes/no)? ").lower()
            if continue_input != "yes":
                break

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")