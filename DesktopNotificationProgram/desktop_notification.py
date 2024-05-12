# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Desktop Notification Program.

Input:
- No specific input required from the user.

Output:
- Displays desktop notifications with a title and message.

Features:
- Shows desktop notifications with customizable title and message.
- Allows customization of notification duration.
- Supports custom icons for notifications.
- Plays a notification sound when displayed.
- Provides options for persistent notifications and clickable notifications with specified URLs.

"""

from plyer import notification
import time
import os
import pygame
from pathlib import Path

def show_notification(title: str, message: str, icon_path: str, sound_path: str, duration: int = 3, persistent: bool = False, clickable: bool = False, url: str = '') -> None:
    """
    Display a desktop notification with customizable options.

    Args:
    - title (str): Title for the notification.
    - message (str): Message content for the notification.
    - duration (int): Duration of the notification in seconds.
    - icon_path (str): Path to a custom icon for the notification.
    - sound_path (str): Path to a notification sound file.
    - persistent (bool): Whether the notification should be persistent.
    - clickable (bool): Whether the notification should be clickable.
    - url (str): URL to open when the notification is clicked.

    Returns:
    - None
    """
    notification_settings = {
        'title': title,
        'message': message,
        'timeout': duration,
        'app_name': 'YourAppName',  # Customize with your app name
    }

    if icon_path:
        notification_settings['app_icon'] = icon_path

    try:
        notification.notify(**notification_settings)  # type:ignore

        if sound_path:
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                time.sleep(duration)
                pygame.mixer.music.stop()
            except Exception as e:
                print(f"Error playing sound: {e}")

        if persistent:
            # Wait for the duration if not persistent
            time.sleep(duration)

        if clickable:
            # Make the notification clickable (Windows-specific)
            os.system(f'start {url}')

    except Exception as e:
        print(f"Error displaying notification: {e}")


if __name__ == '__main__':
    title = "Hello from Python!"
    message = "This is a desktop notification created using Python."

    # Provide the correct absolute paths to the icon and sound files.
    icon_path = str(Path.cwd() / 'Icons' / 'icon.ico')
    sound_path = str(Path.cwd() / 'Sounds' / 'sound.mp3')

    show_notification(
        title,
        message,
        icon_path=icon_path,
        sound_path=sound_path,
        duration=5,
        persistent=True,
        clickable=True,
        url='https://www.python.org/'
    )