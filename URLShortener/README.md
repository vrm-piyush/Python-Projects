# URL Shortener Program

![URL Shortner](image.png)

## Project Overview

The URL Shortener Program is a Python application that leverages the TinyURL API to shorten long URLs. It provides features such as URL shortening, user authentication, rate limiting, URL title extraction, short URL details storage, expiration time settings, redirect type selection, URL categorization, and QR code generation. Users can also edit details of shortened URLs and view a list of their shortened URLs.

## Features

- **URL Shortening:**

  - Shorten long URLs using the TinyURL API.

- **User Authentication:**

  - Authenticate users based on their username and password.

- **Rate Limiting:**

  - Implement rate limiting to prevent abuse (10 requests per minute).

- **URL Title Extraction:**

  - Extract the title of the destination URL for improved user experience.

- **Short URL Details Storage:**

  - Store details of shortened URLs per user, including timestamp and category.

- **Expiration Time Setting:**

  - Allow users to set an expiration time for the short URL.

- **Redirect Type Selection:**

  - Enable users to choose between 301 (permanent) or 302 (temporary) redirection.

- **URL Categorization:**

  - Provide an option for users to categorize their short URLs.

- **QR Code Generation:**

  - Generate QR codes for the shortened URLs for easy sharing and access.

- **URL Editing:**

  - Allow users to edit details of a shortened URL, including the destination URL and category.

- **List Shortened URLs:**

  - Display a list of shortened URLs for a given user.

## How to Use

1. **Run the program:**

   ```bash
   python url_shortener.py [long_url] [expiration_hours] [redirect_type] [username] [password] [category]
   ```

2. **Give input parameters:**

   - Provide the required input parameters such as the long URL, expiration hours, redirect type, username, password, and category.

3. **Short URL Output:**:

   - The program will output the short URL along with additional details such as the URL title.

## Example

```bash
cd URLShortener
python python url_shortener.py https://www.google.co.in/ 48 302 user1 password1
```

```python
QR code generated for https://tinyurl.com/9wm3be2

Long URL: https://www.google.co.in/
Short URL: https://tinyurl.com/9wm3be2

Title: Google

Shortened URLs for User 'user1':
        Original URL: https://www.google.co.in/
        Short URL: https://tinyurl.com/9wm3be2
        Category: No Category
        Timestamp: 2024-03-03 00:24:24.105257
```

## Features to be Added

- **Link Analytics:**

  - Track and display advanced analytics for shortened URLs, including click-through rates and geographic information.

- **Social Media Sharing:**

  - Integrate built-in sharing options for popular social media platforms to enhance sharing capabilities.

- **Link Preview:**

  - Provide a preview of the destination URL when generating the short URL to increase user confidence.

- **URL Shortening API Integration:**

  - Integrate with other URL shortening APIs to offer users more choices and potential additional features.

- **Bulk URL Shortening:**

  - Enable users to shorten multiple URLs at once, especially useful for businesses and marketers.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/Acronym/issues) or refer to [contribution guidelines](../CONTRIBUTING.md) for more details.

---