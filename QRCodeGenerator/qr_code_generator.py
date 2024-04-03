"""
QR Code Generator Program.

Input:
- Type of data: Text or URL to be encoded.
- Output filename for the generated QR code.

Features:
- Batch Processing: Read data from a batch file for multiple QR code generations.
- Logo Embedding: Option to embed a logo or image in the QR code.
"""

import os
import pyqrcode
from PIL import Image
import cv2

def validate_data(data_type, data):
    """
    Validate the user-provided data based on the chosen data type.

    Args:
    - data_type (int): Type of data (1 for Text, 2 for URL).
    - data (str): User-provided data.

    Returns:
    - bool: True if the data is valid, False otherwise.
    """
    if data_type == 1:
        # Validate text data (could add more specific checks if needed).
        return bool(data.strip())
    elif data_type == 2:
        # Validate URL (simple check for 'http://' or 'https://').
        return data.startswith('http://') or data.startswith('https://')
    else:
        return False

def create_qr_code(data, filename, error_correction, logo_path=None, size=None, version=None, output_format='png'):
    """
    Create a QR code for the given data and save it as an image with the specified format.

    Args:
    - data (str): The text or URL to be encoded in the QR code.
    - filename (str): The name of the output file to save the QR code image.
    - error_correction (str): Error correction level ('L', 'M', 'Q', or 'H').
    - logo_path (str): Path to the logo/image file for embedding (None if not provided).
    - size (int): Size adjustment factor (None for default size).
    - version (int): QR code version (None for default version).
    - output_format (str): Output format for the QR code image (default is 'png').
    """
    
    # Generate the QR code using the provided data.
    qr = pyqrcode.create(data, error=error_correction, version=version)
    
    # Create the "QRCodes" folder if it doesn't exist.
    if not os.path.exists("QRCodes"):
        os.makedirs("QRCodes")
    
    # Specify the complete path for the output filename within the "QRCodes" folder.
    output_path = os.path.join("QRCodes", filename)

    # Ensure that the directory exists before attempting to save the file.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the generated QR code as an image with the specified format.
    if output_format.lower() == 'png':
        img = qr.png(output_path, scale=10 if size is None else size)
    elif output_format.lower() == 'eps':
        qr.eps(output_path, scale=10 if size is None else size)
    else:
        print(f"Unsupported output format: {output_format}. Defaulting to PNG.")
        img = qr.png(output_path, scale=10 if size is None else size)

    # Open the image and convert it to RGBA format for color customization.
    img = Image.open(output_path).convert("RGBA")

    datas = img.getdata()
    new_data = []

    for item in datas:
        if item[0]==255 and item[1] == 255 and item[2] == 255:
            new_data.append((255,255,255,0))
        else:
            new_data.append(item)

    # Resize the image if a size adjustment factor is provided.
    if size is not None:
        img = img.resize((size * 10, size * 10))
    
    if logo_path and os.path.exists(logo_path):
        # Open the logo file and paste it onto the QR code image.
        with open(logo_path, 'rb') as logo_file:
            logo = Image.open(logo_file)
            img.paste(logo, (img.width // 4, img.height // 4), logo)

    img.putdata(new_data)
    img.save(output_path)

def read_qr_code(image_path):
    """
    Read and decode a QR code from an image.

    Args:
    - image_path (str): Path to the image containing the QR code.

    Returns:
    - str: Decoded data from the QR code.
    """
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    _, decoded_data, _ = detector.detectAndDecode(img)
    return decoded_data

def single_processing():
    data_type = int(input("\nType of data to encode\n1. Text\n2. URL\nEnter your choice: "))
    if data_type not in [1, 2]:
        print("Invalid data type selected. Exiting.")
        exit()

    data = input("Enter the data to encode: ")
    if not validate_data(data_type, data):
        print("Invalid data. Exiting.")
        exit()

    error_correction_levels = ['L', 'M', 'Q', 'H']
    error_correction = input(f"Choose the error correction level ({', '.join(error_correction_levels)}): ").upper()

    if error_correction not in error_correction_levels:
        print("Invalid error correction level. Exiting.")
        exit()
    
    output_filename = input("Enter the output filename (include extension, e.g., output.png): ")
    
    logo_path = input("Enter the path to the logo/image file for embedding (leave empty if none): ").strip()
    size = input("Enter the size adjustment factor (leave empty for default size): ")
    version = input("Enter the QR code version (leave empty for default version): ")

    output_format = input("Choose the output format ('png', 'eps'): ").lower()

    create_qr_code(data, output_filename, error_correction, logo_path, int(size) if size.isdigit() else None, int(version) if version.isdigit() else None, output_format)

    print(f"QR code generated and saved in 'QRCodes' folder as {output_filename}")

def batch_processing():
    """
    Process multiple QR code generations from a batch file.
    """
    try:
        with open("batch_data.txt", "r") as file:
            for line in file:
                data, output_filename = map(str.strip, line.split(','))
                data_type = 1 if data.startswith('http://') or data.startswith('https://') else 2

                if not validate_data(data_type, data):
                    print(f"Invalid data in batch file: {data}. Exiting.")
                    exit()

                error_correction_levels = ['L', 'M', 'Q', 'H']
                error_correction = input(f"Choose the error correction level ({', '.join(error_correction_levels)}): ").upper()

                if error_correction not in error_correction_levels:
                    print("Invalid error correction level. Exiting.")
                    exit()

                logo_path = input("Enter the path to the logo/image file for embedding (leave empty if none): ").strip()
                size = input("Enter the size adjustment factor (leave empty for default size): ")
                version = input("Enter the QR code version (leave empty for default version): ")
                
                output_format = input("Choose the output format ('png', 'eps'): ").lower()

                create_qr_code(data, output_filename, error_correction, logo_path, int(size) if size.isdigit() else None, int(version) if version.isdigit() else None, output_format)
                print(f"QR code generated and saved as {output_filename}")

    except FileNotFoundError:
        print("\nBatch data file not found.")
        create_file = input("Do you want to create a new batch data file? (yes/no): ").lower()
        
        if create_file == 'yes':
            with open("batch_data.txt", "w") as file:
                while True:
                    data_type = int(input("\nType of data to encode\n1. Text\n2. URL\nEnter your choice: "))
                    if data_type not in [1, 2]:
                        print("Invalid data type selected. Exiting.")
                        return

                    data = input("Enter the data to encode: ")
                    if not validate_data(data_type, data):
                        print("Invalid data. Skipping.")
                        continue
                    
                    filename = input("Enter the output filename (include extension, e.g., output.png): ")
                    file.write(f"{data},{filename}\n")
                    print("Data added to batch file.")
                    
                    add_more = input("Do you want to add more data? (yes/no): ").lower()
                    if add_more != 'yes':
                        break

                print("Batch data file created.")
            batch_processing()
        else:
            print("Exiting.")
    except Exception as e:
        print(f"An error occurred during batch processing: {e}. Exiting.")

if __name__ == "__main__":
    try:
        mode = int(input("Mode\n1. Single QR Code Generation\n2. Batch Processing\nEnter your choice: "))
    except ValueError:
        print("Invalid choice. Exiting.")
        exit()

    if mode == 1:
        single_processing()
    elif mode == 2:
        batch_processing()
    else:
        print("Invalid mode selected. Exiting.")