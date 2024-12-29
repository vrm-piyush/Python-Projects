# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Image to Pencil Sketch Program.

Input:
- Image file path.

Output:
- Pencil Sketch of the image.
- Displays intermediate steps such as grayscale, inversion, and blurred images.

Features:
1. Display the image in a window.
2. Save the image to a specified output path.
3. Convert the input image to a pencil sketch and save different versions.
4. Process all images in the input folder.
5. GUI for interactive image to pencil sketch conversion with parameter customization.

Usage:
- Run the script, and a GUI will appear for selecting input and output folders, setting parameters, and converting images.

"""

import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox


def display_image(image, window_name="Image"):
    """Display the image in a window."""
    cv2.imshow(window_name, image)
    cv2.waitKey(0)

def save_image(image, output_path):
    """Save the image to the specified output path."""
    cv2.imwrite(output_path, image)


def image_to_pencil_sketch(input_image_path, output_folder, blur_kernel_size=21, scaling_factor=256.0, color_pencil=False,
                            save_grayscale=True, save_pencil_sketch=True):
    """Convert the input image to a pencil sketch and save different versions."""
    # Read the input image
    image = cv2.imread(input_image_path)

    if image is None:
        raise Exception(f"Error: Unable to load the image at {input_image_path}")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_image = cv2.bitwise_not(gray_image)

    # Apply Gaussian Blur to the inverted image
    blurred_image = cv2.GaussianBlur(inverted_image, (blur_kernel_size, blur_kernel_size), 0)

    # Invert the blurred image
    inverted_blurred = cv2.bitwise_not(blurred_image)

    # Create the pencil sketch by dividing the grayscale image by the inverted blurred image
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=scaling_factor)

    # Convert the pencil sketch to three channels
    pencil_sketch_colored = cv2.cvtColor(pencil_sketch, cv2.COLOR_GRAY2BGR)

    # Save the images based on user preferences
    filename = os.path.splitext(os.path.basename(input_image_path))[0]
    if save_grayscale:
        save_image(gray_image, os.path.join(output_folder, f"{filename}_grayscale.jpg"))
    if save_pencil_sketch:
        if color_pencil:
            # Blend the color information with the pencil sketch
            color_sketch = cv2.addWeighted(image, 0.5, pencil_sketch_colored, 0.5, 0)
            save_image(color_sketch, os.path.join(output_folder, f"{filename}_color_pencil_sketch.jpg"))
        else:
            save_image(pencil_sketch_colored, os.path.join(output_folder, f"{filename}_pencil_sketch.jpg"))


def process_images(input_folder, output_folder, blur_kernel_size, scaling_factor, color_pencil,
                   save_grayscale, save_pencil_sketch):
    """Process all images in the input folder."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            input_image_path = os.path.join(input_folder, filename)
            output_sketch_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_sketch.jpg")
            print(f"Processing: {input_image_path}")
            image_to_pencil_sketch(input_image_path, output_sketch_path, blur_kernel_size, scaling_factor, color_pencil, save_grayscale, save_pencil_sketch)
        else:
            print(f"Skipping {filename} - File format not supported")

class ImageToPencilSketchGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Image to Pencil Sketch Converter")

        # Create input and output folder paths
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()

        # Set default values for input and output folders
        self.input_folder.set("Input")
        self.output_folder.set("Output")

        # Create parameters
        self.blur_kernel_size = tk.IntVar()
        self.scaling_factor = tk.DoubleVar()
        self.color_pencil = tk.BooleanVar()
        self.save_grayscale = tk.BooleanVar()
        self.save_pencil_sketch = tk.BooleanVar()

        # Set default values for parameters
        self.blur_kernel_size.set(21)
        self.scaling_factor.set(256.0)
        self.color_pencil.set(False)
        self.save_grayscale.set(True)
        self.save_pencil_sketch.set(True)

        # Create GUI elements
        tk.Label(root, text="Input Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.input_folder, state="readonly", width=30).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_input_folder).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.output_folder, state="readonly", width=30).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(root, text="Blur Kernel Size:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.blur_kernel_size, width=10).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Scaling Factor:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.scaling_factor, width=10).grid(row=3, column=1, padx=5, pady=5)

        tk.Checkbutton(root, text="Color Pencil", variable=self.color_pencil).grid(row=2, column=2, padx=5, pady=5)
        tk.Checkbutton(root, text="Save Grayscale", variable=self.save_grayscale).grid(row=3, column=2, padx=5, pady=5)
        tk.Checkbutton(root, text="Save Pencil Sketch", variable=self.save_pencil_sketch).grid(row=4, column=2, padx=5, pady=5)

        tk.Button(root, text="Convert Images", command=self.convert_images).grid(row=4, column=1, pady=10)
        tk.Button(root, text="Quit", command=root.destroy).grid(row=5, column=1, pady=10)
    
    def browse_input_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_folder.set(folder_selected)

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder.set(folder_selected)

    def convert_images(self):
        try:
            blur_kernel_size = self.blur_kernel_size.get()
            scaling_factor = self.scaling_factor.get()
            color_pencil = self.color_pencil.get()
            save_grayscale = self.save_grayscale.get()
            save_pencil_sketch = self.save_pencil_sketch.get()
            process_images(self.input_folder.get(), self.output_folder.get(), blur_kernel_size, scaling_factor, color_pencil, save_grayscale, save_pencil_sketch)
            messagebox.showinfo("Conversion Complete", "Image conversion to pencil sketch is complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageToPencilSketchGUI(root)
    root.mainloop()