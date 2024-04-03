
import csv, os, logging, sys
from datetime import datetime
from itertools import dropwhile, takewhile
from instaloader.structures import Profile, Hashtag
from instaloader.instaloader import Instaloader
import instaloader

class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = Instaloader()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def hardcoded_login(self, username, password):
        self.L.context.username = username
        session_filename = f"session-{username}"

        try:
            self.L.load_session_from_file(session_filename)
        except FileNotFoundError:
            # Try to load session file from the user's temporary directory
            temp_dir = os.getenv("TEMP") or os.getenv("TMP")  # Check both TEMP and TMP environment variables
            temp_session_file = os.path.join(temp_dir, f".instaloader-{username}")

            try:
                self.L.load_session_from_file(temp_session_file)
            except FileNotFoundError:
                self.logger.info(f"Session file not found for user {username}. Logging in manually.")

                try:
                    self.L.context.password = password
                    self.L.interactive_login(username)
                except instaloader.exceptions.TwoFactorAuthRequiredException:
                    code = input("Enter 2FA verification code: ")
                    self.L.context.two_factor_code = code
                    self.L.login(username, password)
                except instaloader.exceptions.LoginException as e:
                    self.logger.error(f"Login failed: {e}")
                    sys.exit(1)

                self.save_session(username)

    def save_session(self, username):
        # Save the session after successful login
        self.L.save_session_to_file(username)

    def download_users_profile_picture(self, username):
        self.L.load_session_from_file(username)
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periods(self, username):
        self.L.load_session_from_file(username)
        posts = Profile.from_username(self.L.context, username).get_posts()
        SINCE = datetime(2022, 1, 1)
        UNTIL = datetime(2024, 1, 31)

        for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
            self.L.download_post(post, target=username)

    def download_hashtag_posts(self, hashtag):
        self.L.load_session_from_file(self.L.context.username or "")
        for post in Hashtag.from_name(self.L.context, hashtag).get_posts():
            self.L.download_post(post, target='#'+hashtag)

    def fetch_users_followers(self, user_name):
        self.L.load_session_from_file(user_name)
        profile = Profile.from_username(self.L.context, user_name)
        file_path = "follower_names.txt"
        with open(file_path, 'a+') as file:
            for followee in profile.get_followers():
                follower_username = followee.username
                file.write(follower_username + '\n')
                self.logger.info(follower_username)

    def fetch_users_followings(self, user_name):
        self.L.load_session_from_file(user_name)
        profile = Profile.from_username(self.L.context, user_name)
        file_path = "following_names.txt"
        with open(file_path, 'a+') as file:
            for followee in profile.get_followees():
                following_username = followee.username
                file.write(following_username + "\n")
                self.logger.info(following_username)

    def get_post_comments(self, username):
        self.L.load_session_from_file(username)
        posts = Profile.from_username(self.L.context, username).get_posts()
        for post in posts:
            for comment in post.get_comments():
                self.logger.info(f"comment.id  : {comment.id}")
                self.logger.info(f"comment.owner.username  : {comment.owner.username}")
                self.logger.info(f"comment.text  : {comment.text}")
                self.logger.info(f"comment.created_at_utc  : {comment.created_at_utc}")
                self.logger.info("************************************************")

    def get_post_info_csv(self, username):
        self.L.load_session_from_file(username)
        file_path = f"{username}.csv"
        with open(file_path, 'a+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            posts = Profile.from_username(self.L.context, username).get_posts()
            for post in posts:
                self.logger.info(f"post date: {post.date}")
                self.logger.info(f"post profile: {post.profile}")
                self.logger.info(f"post caption: {post.caption}")
                self.logger.info(f"post location: {post.location}")
                
                post_url = f"https://www.instagram.com/p/{post.shortcode}"
                self.logger.info(f"post url: {post_url}")
                
                writer.writerow(["post", post.mediaid, post.profile, post.caption, post.date, post.location,
                                 post_url, post.typename, post.mediacount, post.caption_hashtags,
                                 post.caption_mentions, post.tagged_users, post.likes, post.comments,
                                 post.title, post.url])

                for comment in post.get_comments():
                    writer.writerow(["comment", comment.id, comment.owner.username, comment.text, comment.created_at_utc])
                    self.logger.info(f"comment username: {comment.owner.username}")
                    self.logger.info(f"comment text: {comment.text}")
                    self.logger.info(f"comment date: {comment.created_at_utc}")

                self.logger.info("\n\n")

    def main_menu(self, username, password):
        self.hardcoded_login(username,password)

        print("\nChoose an option:")
        print("1. Download User's Profile Picture")
        print("2. Download User's Posts within a Period")
        print("3. Download Hashtag Posts")
        print("4. Fetch User's Followers")
        print("5. Fetch User's Followings")
        print("6. Get Post Comments")
        print("7. Get Post Info CSV")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            self.download_users_profile_picture(username)
        elif choice == '2':
            self.download_users_posts_with_periods(username)
        elif choice == '3':
            hashtag = input("Enter the hashtag you want to download posts for: ")
            self.download_hashtag_posts(hashtag)
        elif choice == '4':
            self.fetch_users_followers(username)
        elif choice == '5':
            self.fetch_users_followings(username)
        elif choice == '6':
            self.get_post_comments(username)
        elif choice == '7':
            self.get_post_info_csv(username)
        elif choice == '8':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    hardcode_username = "__unfiltered__thoughts__"
    
    if len(sys.argv)!=2:
        print("Usage: python secript.py <password>")
        sys.exit(1)
    
    hardcoded_password = sys.argv[1]

    cls = GetInstagramProfile()
    while True:
        cls.main_menu(hardcode_username, hardcoded_password)
