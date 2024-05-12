# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Alarm Clock Program.

Input:
- Time.

Output:
- Alarm sound.

Features:
- Allows the user to set an alarm by entering the desired time in the format (HH:MM:SS AM/PM).
- Validates the format and components of the entered alarm time.
- Uses the 'pygame' library to play an alarm sound when the set time is reached.
- Displays a wake-up message when the alarm is triggered.

"""

from datetime import datetime
import pygame.time

def validate_time(alarm_time: str) -> str:
    """
    Validate the format of the entered alarm time.

    Args:
    - alarm_time (str): The entered alarm time string.

    Returns:
    - str: Message indicating the validation status.
    """

    # Check if the length of the time string is not equal to 11 characters.
    if len(alarm_time) != 11:
        return "Invalid time format! Please try again..."
    
    # Extract hours, minutes, and seconds from the entered time string and validate them.
    elif int(alarm_time[0:2]) > 12 or int(alarm_time[3:5]) > 59 or int(alarm_time[6:8]) > 59:
        return "Invalid time components! Please try again..."
    else:
        return "ok"

if __name__ == '__main__':
    # Loop to get a valid alarm time from the user.
    while True:
        alarm_time = input("Enter the time of alarm to be set in 12-hour format (HH:MM:SS AM/PM): ").strip()
        
        # Validate the entered alarm time.
        validate_status = validate_time(alarm_time.lower())
        
        # If the time is invalid, display the error message and continue the loop.
        if validate_status != "ok":
            print(validate_status)
        else:
            print(f"Setting alarm for {alarm_time}...")
            
            # Extract and convert time components for setting the alarm.
            alarm_parts = alarm_time.split()
            alarm_hour, alarm_minute, alarm_seconds = map(int, alarm_parts[0].split(':'))
            alarm_period = alarm_parts[1].upper()
            
            break  # Exit the loop once a valid alarm time is set.

    # Loop to continuously check if the current time matches the set alarm time.
    while True:
        # Get the current system time.
        now = datetime.now()
        
        # Extract current hour, minute, second, and period (AM/PM).
        current_hour, current_minute, current_seconds, current_period = now.strftime("%I"), now.strftime("%M"), now.strftime("%S"), now.strftime("%p").upper()

        # Check if the current time matches the set alarm time.
        if alarm_period == current_period and alarm_hour == int(current_hour) and alarm_minute == int(current_minute) and alarm_seconds == int(current_seconds):
            print("Wake Up!!")
            
            # Play the alarm sound.
            pygame.mixer.init()
            pygame.mixer.music.load('have_a_nice_day-alarm.wav')
            pygame.mixer.music.play()
            pygame.time.wait(18000)
            pygame.mixer.music.stop()

            break  # Exit the loop once the alarm is triggered.