# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Using Phone Camera for Computer Vision Program.

Input:
- Enter the IP Address.

Output:
- Opens the phone camera and displays the video feed.

Features:
- Captures video frames from the phone's camera using the specified IP address.
- Utilizes the IP Webcam server running on the phone to fetch image frames.
- Displays the captured frames in an OpenCV window.
- Allows the user to exit the program by pressing the 'Esc' key.

"""

import cv2
import numpy as np
import requests
import imutils

def capture_from_phone_camera(ip_address: str) -> None:
    """
    Capture video frames from the phone's camera using the specified IP address.
    
    Args:
    - ip_address (str): IP address where the phone camera server is running.
    
    Returns:
    - None
    """
    # Construct the complete URL by appending the endpoint to the entered IP address.
    url = f"{ip_address}/shot.jpg"

    # Continuously capture and display frames from the phone's camera.
    while True:
        # Fetch the image from the IP Webcam server running on the phone.
        img_resp = requests.get(url)
        
        # Convert the binary image data into a format that OpenCV can handle.
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        
        # Resize the image for better display (optional based on requirements).
        img = imutils.resize(img, width=1000, height=1800)
        
        # Display the image in an OpenCV window named "Android Camera".
        cv2.imshow("Android Camera", img)

        # Check for the 'Esc' key press to exit the loop and close the window.
        key = cv2.waitKey(1)
        if key == 27:  # 'Esc' key
            break

    # Destroy all OpenCV windows and release resources.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    """
    Main function to capture the IP address and initiate the video capture process.
    """
    try:
        # Prompt the user to enter the IP address of the phone's camera server.
        ip_address = input("Enter the IP Address (e.g., http://192.168.0.103:8080): ").strip()
        
        # Start capturing video frames from the phone's camera using the provided IP address.
        capture_from_phone_camera(ip_address)
    
    except Exception as e:
        # Handle any exceptions that may occur during execution.
        print(f"An error occurred: {e}")
        print("Exiting the program...")
        cv2.destroyAllWindows()