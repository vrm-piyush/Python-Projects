# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Barcode and QR code reader Program.

Input:
- Barcode or QR code.

Output:
- Displays the camera feed with recognized barcode information.

Features:
- Provides a GUI for scanning and recognizing barcodes and QR codes using a camera feed.
- Allows users to start and stop the scanning process.
- Recognizes and displays barcode information on the camera feed.
- Customizable scanning status labels.
- Saves recognized barcode information along with timestamps to a text file.
- Generates a beep sound on successful scanning (Windows only).

Note: Ensure that the necessary libraries (OpenCV and pyzbar) are installed.

"""

import cv2
from pyzbar import pyzbar
import os
import datetime
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class BarcodeQRCodeReaderApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.camera = cv2.VideoCapture(0)
        self.recognized_barcodes = set()

        # Create GUI elements
        self.start_button = ttk.Button(window, text="Start Scanning", command=self.start_scanning)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(window, text="Stop Scanning", command=self.stop_scanning)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        # Set up the video display
        self.video_label = tk.Label(window)
        self.video_label.grid(row=1, column=0, columnspan=2)

        # Set up the scanning status label
        self.status_label = tk.Label(window, text="Scanning status: Stopped", font=("Arial", 12))
        self.status_label.grid(row=2, column=0, columnspan=2)

        # Bind closing event to stop scanning
        self.window.protocol("WM_DELETE_WINDOW", self.stop_scanning)
    
    def start_scanning(self):
        """Start the scanning process."""
        self.status_label.config(text="Scanning status: Started")
        self.scan()

    def stop_scanning(self):
        """Stop the scanning process and release the camera."""
        self.status_label.config(text="Scanning status: Stopped")
        self.camera.release()
        self.window.destroy()
    
    def scan(self):
        """Scan for barcodes and QR codes in the camera feed."""
        if self.status_label.cget("text") == "Scanning status: Started":
            ret, frame = self.camera.read()

        try:
            frame = self.read_barcodes(frame)
        except Exception as e:
            print(f"Error: {e}")

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = self.convert_cv2_to_tkinter_image(cv2image)

        # Update the video display
        self.video_label.img = img # type: ignore
        self.video_label.configure(image=img)

        # Continue scanning if not stopped
        if self.status_label.cget("text") == "Scanning status: Started":
            self.window.after(10, self.scan)

    def convert_cv2_to_tkinter_image(self, cv2_image):
        """Convert a cv2 image to a Tkinter image with enhanced color and brightness."""
        img = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        # Enhance color and brightness (adjust as needed)
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=25)
        
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        return img
    
    def read_barcodes(self,frame):
        """Read barcodes and QR codes from the camera feed."""
        try:
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                x, y, w, h = barcode.rect
                barcodes_info = barcode.data.decode('utf-8')

                # Check if the barcode has already been recognized
                if barcodes_info not in self.recognized_barcodes:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, barcodes_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

                    # Display additional information based on the barcode content
                    if barcode.type == 'QRCODE':
                        if barcodes_info.startswith('BEGIN:VCARD'):
                            # Extract contact information from a vCard QR code
                            vcard_info = barcodes_info.split('\n')
                            additional_info_displayed = False
                            for line in vcard_info:
                                if line.startswith('FN:'):
                                    additional_info = f"Contact Name: {line[3:]}"
                                    cv2.putText(frame, additional_info, (x + 6, y + h + 30), font, 1.0, (255, 255, 255), 1)
                                    additional_info_displayed = True
                                
                            if additional_info_displayed:
                                self.recognized_barcodes.add(barcodes_info)

                    # Display code type
                    code_type = barcode.type

                    with open("result.txt", mode='a') as file:
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # Add timestamp
                        file.write(f"{timestamp} - Recognized {code_type} Code: {barcodes_info}\n")

                    # Beep sound on successful scanning
                    if os.name == 'nt':
                        import winsound
                        winsound.Beep(1000, 200)  # Frequency: 1000 Hz, Duration: 200 ms

                    # Add the barcode to the set of recognized barcodes
                    self.recognized_barcodes.add(barcodes_info)
        except Exception as e:
            print(f'Error: {e}')

        return frame

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeQRCodeReaderApp(root, "Barcode/QR Code Reader")
    root.mainloop()


"""
To enhance your barcode and QR code reader program, you can consider adding the following features:

1. **Multiple Code Recognition:**
   Extend the program to recognize and decode multiple barcodes or QR codes in a single frame. This is especially useful when there are multiple codes in the camera's field of view.

2. **Code Type Identification:**
   Implement code type identification to distinguish between barcodes and QR codes. Display the code type along with the decoded information.

3. **User Interface:**
   Create a simple GUI (Graphical User Interface) to provide a more user-friendly experience. This can include buttons for starting and stopping the scanning process.

4. **Code History Logging:**
   Maintain a history log of recognized codes with timestamps. Save this information to a file or database for later reference.

5. **Code Filtering:**
   Allow the user to filter or ignore certain types of codes. For example, the ability to exclude specific QR codes based on their content.

6. **Continuous Scanning:**
   Implement continuous scanning where the program continuously captures frames and scans for codes. This can be useful for scenarios where codes are frequently changing.

7. **Error Handling and Logging:**
   Improve error handling and logging mechanisms to provide detailed information about any errors encountered during code recognition.

8. **Configuration Options:**
   Add configuration options to customize the program's behavior, such as camera selection, resolution settings, and decoding options.

9. **Code Highlighting:**
   Highlight the recognized codes in a visually distinct way, such as changing the border color or adding a bounding box around the codes.

10. **Code Content Display:**
    Display additional information about the decoded code content. For instance, display contact information for a QR code that represents a vCard.

11. **Integration with External Systems:**
    Integrate the program with external systems or databases to perform actions based on the decoded code information. For example, trigger a web API call or update a database.

12. **Code Filtering based on Location:**
    Implement location-based filtering where certain codes are recognized only if they are within a specified geographical region.

Remember to consider the specific use case and requirements of your application when selecting features to implement.
"""

