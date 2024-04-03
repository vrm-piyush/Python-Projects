"""
URL Shortener Program.

Input:
- A long URL to be shortened.

Output:
- A shortened URL using the TinyURL API.

Features:
- URL shortening using the TinyURL API.
- User authentication based on username and password.
- Rate limiting to prevent abuse (10 requests per minute).
- URL title extraction from the destination URL.
- Short URL details storage per user, including timestamp and category.
- Option to set expiration time for the short URL.
- Option to choose redirect type (301 or 302).
- Option to categorize the short URL.
- QR code generation for the short URL.
- Ability to edit details of a shortened URL.
- Display a list of shortened URLs for a given user.

Usage:
- python 25.%20URLShortener.py [long_url] [expiration_hours] [redirect_type] [username] [password] [category]

"""

import sys
import validators
import subprocess
from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

users = {'user1':
            {
                'password': 'password1', 
                'short_urls': [],
                'request_count': 0,
                'last_request_time': None
            },
         'user2':
            {
                'password': 'password2', 
                'short_urls': [],
                'request_count': 0,
                'last_request_time': None
            },
}

REQUEST_LIMIT = 10
TIME_INTERVAL = 60

def authenticate_user(username, password):
    """
    Authenticate the user based on the provided username and password.
    """
    user_data = users.get(username)
    if user_data and user_data['password'] == password:
        return True
    return False

def is_valid_url(url):
    return validators.url(url)

def get_url_title(url):
    try:
        with urlopen(url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            title_tag = soup.find('title')
            return title_tag.text.strip() if title_tag else None
    except Exception as e:
        print(f'Error fetching URL title: {e}')
        return None
    
def check_rate_limit(username):
    """
    Check if the user has reached the rate limit for URL shortening.
    """
    user_data = users.get(username)
    if user_data:
        current_time = datetime.now()
        last_request_time = user_data['last_request_time']
        request_count = user_data['request_count']

        if last_request_time and (current_time - last_request_time).seconds < TIME_INTERVAL:
            if request_count >= REQUEST_LIMIT:
                print(f'Rate limit exceeded. Please wait for {TIME_INTERVAL} seconds before making another request.')
                return False
        else:
            user_data['request_count'] = 0
        
        user_data['last_request_time'] = current_time
        user_data['request_count'] += 1
    
    return True

def make_tiny(url, expiration_hours=None, redirect_type=None, username=None, password=None, category=None):
    if not check_rate_limit(username):
        return None, None
    
    api_url = 'http://tinyurl.com/api-create.php'

    if username and password and not authenticate_user(username, password):
        print('Authentication failed. Please check your username and password.')
        return None, None

    params = {
        'url': url
    }

    if expiration_hours is not None:
        expiration_time = datetime.now() + timedelta(hours=expiration_hours)
        params['expires'] = expiration_time.strftime('%Y-%m-%d %H:%M:%S')

    if redirect_type in ['301', '302']:
        params['type'] = redirect_type

    if category is not None:
        params['category'] = category

    encoded_params = urlencode(params).encode('utf-8')  # Encode the parameters
    
    with urlopen(api_url, encoded_params) as response:
        short_url = response.read().decode('utf-8')

        # Fetch the title of the destination URL
        url_title = get_url_title(url)

        if username and username in users:
            if category is None:
                users[username]['short_urls'].append({'original_url': url, 'short_url': short_url, 'timestamp': datetime.now()})
            else:
                users[username]['short_urls'].append({'original_url': url, 'short_url': short_url, 'timestamp': datetime.now(), 'category': category})

        # Generate a QR code for the short URL.
        generate_qr_code(short_url, 'qr_code_url.png', 'H', '', '', '', 'png')

        return short_url, url_title
    
def edit_short_url(username, short_url):
    """
    Allow user to edit the details of a shortened URL.
    """

    if username not in users:
        print(f"User '{username}' not found.")
        return
    
    user_urls = users[username]['short_urls']

    for entry in user_urls:
        if entry.get['short_url'] == short_url:
            print(f"Editing Short URL: {short_url}")
            new_destination_url = input('Enter the new destination URL: ')
            new_category = input('Enter the new category (leave empty to keep the current category): ')

            entry['original_url'] = new_destination_url
            if new_category:
                entry['category'] = new_category
            
            print('Short URL details updated successfully.')
            return
        
        print(f"Short URL '{short_url}' not found for user '{username}'.")
    
def list_user_urls(username):
    """
    Display a list of shortened URLs for the given user.
    """

    if username not in users:
        print(f"User '{username}' not found.")
        return

    user_urls = users[username]['short_urls']

    if not user_urls:
        print(f"No shortened URLs found for user '{username}'.")
    else:
        print(f"Shortened URLs for User '{username}':")
        for entry in user_urls:
            print(f"\tOriginal URL: {entry.get('original_url', 'N/A')}")
            print(f"\tShort URL: {entry.get('short_url', 'N/A')}")
            print(f"\tCategory: {entry.get('category', 'No Category')}")
            print(f"\tTimestamp: {entry.get('timestamp', 'N/A')}\n")
    
def generate_qr_code(data, output_filename, error_correction, logo_path, size, version, output_format):
    """
    Generate a QR code for the given data. 
    """

    try:
       # Prepare the input string for the external script
        input_string = f"1\n2\n{data}\n{error_correction}\n{output_filename}\n{logo_path}\n{size}\n{version}\n{output_format}\n"

        # Run the external script 'qr_code_generator.py' with the input provided
        subprocess.run(['python', 'C:\\Users\\ashok\\source\\Python 60 Projects\\QRCodeGenerator\\qr_code_generator.py'], input=input_string, text=True, check=True, stdout=subprocess.DEVNULL)

        print(f"QR code generated for {data}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating QR code: {e}")
    
def main():
    if len(sys.argv) < 2:
        print('Usage: python 25.%20URLShortner.py [long_url] [expiration_hours] [redirect_type] [username] [password] [category]')
        return
    
    long_url = sys.argv[1]

    # Check if the URL is valid
    if not is_valid_url(long_url):
        print('Invalid URL. Please enter a valid URL.')
        return
    
    expiration_hours = None
    redirect_type = None
    username = None
    password = None
    category = None

    if len(sys.argv) == 3:
        expiration_hours = float(sys.argv[2])

    if len(sys.argv) == 4:
        redirect_type = sys.argv[3]

    if len(sys.argv) == 6:
        username = sys.argv[4]
        password = sys.argv[5]
    
    if len(sys.argv) == 7:
        category = str(sys.argv[6])

    short_url, url_title = make_tiny(long_url, expiration_hours, redirect_type, username, password, category)

    print(f'\nLong URL: {long_url}')
    print(f'Short URL: {short_url}\n')   

    if url_title:
        print(f'Title: {url_title}\n') 

    if username:
        list_user_urls(username)

    if username and category:
        edit_option = input('Do you want to edit the details of a shortened URL? (yes/no): ').lower()
        if edit_option == 'yes':
            short_url_to_edit = input('Enter the short URL to edit: ')
            edit_short_url(username, short_url_to_edit)
            list_user_urls(username)

if __name__ == '__main__':
    main()



"""
The order in which you implement these features depends on your specific goals, user base, and resources. However, here's a suggested order that considers a balance between improving functionality and maintaining a positive user experience:

1. **URL Validation:**
   Ensure that the provided URL is valid before attempting to shorten it. This is a fundamental step to prevent errors and enhance user experience.

2. **Link Expiry:**
   Adding link expiration can be a useful feature and can help manage the lifespan of short URLs.

3. **Link Redirection:**
   Allow users to choose between permanent (301) or temporary (302) redirection for their short URLs. This is a basic but important customization option.

4. **Link Analytics:**
   Start tracking and displaying basic analytics for shortened URLs, such as the number of clicks. This provides users with insights into the performance of their links.

5. **QR Code Generation:**
   Generate QR codes for the short URLs, making it easy for users to share and access the link using a QR code scanner.

6. **Social Media Sharing:**
   Add built-in sharing options for popular social media platforms. This enhances the sharing capabilities of your service.

7. **Link Preview:**
   Provide a preview of the destination URL when generating the short URL. This can increase user confidence in the links they share.

8. **URL Shortening API Integration:**
   Integrate with popular URL shortening APIs (e.g., Bitly, Rebrandly) to offer users more choices and potentially additional features.

9. **Bulk URL Shortening:**
   Enable users to shorten multiple URLs at once. This feature can be especially valuable for businesses and marketers.

10. **Custom Short URLs:**
    Allow users to choose a custom short URL. This can be a premium feature or available for registered users.

11. **User Authentication:**
    Implement user accounts and authentication to track and manage shortened URLs. This sets the foundation for personalized features and link management.

12. **Link Management:**
    Offer tools for users to organize, categorize, and manage their shortened URLs effectively. This becomes more crucial as users create and track more links.

13. **Link Editing:**
    Allow users to edit the destination URL or other details of their shortened links after creation. This provides flexibility and correction options.

14. **Browser Extension:**
    Develop a browser extension that allows users to shorten URLs directly from their browser toolbar. This enhances user convenience.

15. **Security Measures:**
    Implement measures to prevent abuse, such as rate limiting, CAPTCHA verification, or additional security checks.

16. **Domain Customization:**
    Allow organizations to use their own domain for URL shortening, providing a branded experience.

17. **Link Sharing Restrictions:**
    Allow users to set restrictions on who can access their short URLs, such as requiring a password or access code.

18. **Link Archiving:**
    Allow users to archive or unarchive their shortened URLs to keep their link lists organized.

19. **Link Import/Export:**
    Support importing and exporting of shortened URLs for backup or migration purposes.

20. **Localization:**
    Support multiple languages and regions to cater to a diverse user base.
"""