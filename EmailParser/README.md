# Email ID Parser

![email parser](../assets/images/readme_images/email_parser.png)

## Project Overview

The Email ID Parser is a Python program designed to extract the username and domain name from an email ID. It validates the format of the input email ID using a simple regular expression, normalizes the email address to lowercase, and handles cases where the domain may have subdomains.

## Features

- **Email Format Validation:**

  - Validates the format of the input email ID using a simple regular expression.

- **Normalization:**

  - Normalizes the email address to lowercase for consistency.

- **Extraction:**

  - Extracts the username, subdomain (if any), and main domain from the email ID.

- **Subdomain Handling:**
  - Handles cases where the domain may have subdomains.

## How to Use

1. **Run the Program:**

   - Execute the program and follow the on-screen prompts.

2. **Enter Email ID:**

   - Enter your email ID when prompted.

3. **Extraction:**

   - The program extracts the username, subdomain (if any), and main domain from the email ID.

4. **Continue or Exit:**
   - Optionally, choose to continue extracting information from more email IDs.

## Example

```bash
cd EmailParser
python email_id_parser.py
```

```python
Enter your Email ID: user@example.com

Username: user
No subdomain
Main Domain: example.com
```

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/EmailParser/issues) or submit a pull request.

---
