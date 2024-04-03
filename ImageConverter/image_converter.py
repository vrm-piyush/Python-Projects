"""
Image Converter GUI Program.

Input:
- Image file path.

Output:
- Converted image file.

Features:
- Image selection using a file dialog.
- Options for output format (JPEG, PNG, GIF, BMP, TIFF).
- Resizing and cropping options.
- Output quality adjustment for JPEG format.
- Display of file information after conversion.
- Status updates for successful or failed conversions.

"""

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os

class ImageConverterApp:
    def __init__(self, root):
        """
        Initialize the Image Converter GUI.

        Args:
        - root: Tkinter root window.
        """
        self.root = root
        self.root.title('Image Converter')

        # Variables
        self.imported_image = None
        self.output_format = tk.StringVar(value="JPEG")  # Default format is JPEG

        # Canvas
        self.canvas = tk.Canvas(root, width=500, height=550, bg='azure3', relief='raised')
        self.canvas.pack()

        # Label
        self.label = tk.Label(root, text='Image Converter', bg='azure3', font=('helvetica', 20))
        self.canvas.create_window(260, 30, window=self.label)

        # Buttons and Entry Widgets
        self.browse_button = tk.Button(root, text='Select Image', command=self.get_image, bg='royalblue',
                                       fg='white', font=('helvetica', 12, 'bold'))
        self.canvas.create_window(260, 80, window=self.browse_button)

        self.format_label = tk.Label(root, text='Output Format:', bg='azure3', font=('helvetica', 12))
        self.canvas.create_window(150, 130, window=self.format_label)

        self.format_menu = ttk.Combobox(root, textvariable=self.output_format,
                                        values=["JPEG", "PNG", "GIF", "BMP", "TIFF"])
        self.canvas.create_window(330, 130, window=self.format_menu)

        # Resize and Crop
        self.resize_label = tk.Label(root, text='Resize (Width x Height):\n\n', bg='azure3', font=('helvetica', 12))
        self.canvas.create_window(180, 190, window=self.resize_label)

        self.width_entry = tk.Entry(root)
        self.canvas.create_window(190, 200, window=self.width_entry)
        self.x_label = tk.Label(root, text='x', bg='azure3', font=('helvetica', 12))
        self.canvas.create_window(265, 200, window=self.x_label)
        self.height_entry = tk.Entry(root)
        self.canvas.create_window(340, 200, window=self.height_entry)

        self.crop_var = tk.BooleanVar(value=False)
        self.crop_checkbox = tk.Checkbutton(root, text='Crop', variable=self.crop_var, bg='azure3',
                                            font=('helvetica', 12))
        self.canvas.create_window(260, 240, window=self.crop_checkbox)

        # Output Quality
        self.quality_label = tk.Label(root, text='Output Quality (1-100):', bg='azure3', font=('helvetica', 12))
        self.canvas.create_window(170, 280, window=self.quality_label)

        self.quality_entry = tk.Entry(root)
        self.canvas.create_window(340, 280, window=self.quality_entry)

        # File Information
        self.info_label = tk.Label(root, text='File Information:', bg='azure3', font=('helvetica', 12))
        self.canvas.create_window(150, 320, window=self.info_label)

        self.info_text = tk.Text(root, height=5, width=35)
        self.canvas.create_window(260, 380, window=self.info_text)

        # Convert Button
        self.convert_button = tk.Button(root, text='Convert', command=self.convert_image, bg='royalblue',
                                        fg='white', font=('helvetica', 12, 'bold'))
        self.canvas.create_window(260, 460, window=self.convert_button)

        # Status Label
        self.status_label = tk.Label(root, text='', bg='azure3', font=('helvetica', 10))
        self.canvas.create_window(260, 500, window=self.status_label)

    def get_image(self):
        """
        Open a file dialog to select an image file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")])
        if file_path:
            self.imported_image = Image.open(file_path)
            self.status_label.config(text=f'Selected: {file_path.split("/")[-1]}')
        else:
            self.status_label.config(text='No file selected')

    def convert_image(self):
        """
        Convert the selected image based on user input.
        """
        if self.imported_image:
            try:
                if 'A' in self.imported_image.getbands():
                    self.imported_image = self.imported_image.convert('RGB')

                output_format = self.output_format.get().lower()
                export_file_path = filedialog.asksaveasfilename(defaultextension=f'.{output_format}',
                                                                filetypes=[(f"{output_format.upper()} files",
                                                                            f"*.{output_format.lower()}")])

                if export_file_path:
                    width = self.width_entry.get()
                    height = self.height_entry.get()

                    if width and height:
                        width, height = int(width), int(height)
                        self.imported_image = self.imported_image.resize((width, height))

                    if self.crop_var.get():
                        # Assuming crop parameters are specified as left, top, right, bottom
                        crop_params = (0, 0, int(width), int(height))
                        self.imported_image = self.imported_image.crop(crop_params)

                    # Output Quality
                    quality = self.quality_entry.get()
                    if quality and output_format == "jpeg":
                        quality = int(quality)
                        if 1 <= quality <= 100:
                            self.imported_image.save(export_file_path, quality=quality)
                        else:
                            raise ValueError("Quality must be between 1 and 100")
                    else:
                        self.imported_image.save(export_file_path)

                    # File Information
                    file_info = f"Dimensions: {self.imported_image.width} x {self.imported_image.height}\n"
                    file_info += f"File Size: {os.path.getsize(export_file_path) / 1024:.2f} KB\n"
                    file_info += f"Color Mode: {', '.join(self.imported_image.getbands())}"
                    self.info_text.delete(1.0, tk.END)  # Clear previous info
                    self.info_text.insert(tk.END, file_info)

                    self.status_label.config(text=f'Conversion successful! Saved as {export_file_path}')
                else:
                    self.status_label.config(text='Conversion canceled')
            except Exception as e:
                self.status_label.config(text=f'Error: {e}')
        else:
            self.status_label.config(text='Please select an image first')

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()