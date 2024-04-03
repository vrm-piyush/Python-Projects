"""
Image Filtering Program.

Input:
- User-provided options for image path and filter choice.

Output:
- Displays original and filtered color/grayscale images.
- Saves filtered images in a 'filtered' folder.

Features:
- Load Image: Allows the user to load an image file (jpg, jpeg, png).
- Resize Image: Resizes the loaded image by a factor of 0.5.
- Choose Filter: Entry for the user to choose a filter type (1: Mean, 2: Gaussian, 3: Median, 4: Custom).
- Apply Filter: Applies the selected filter to the image.
- Apply in Parallel: Checkbox to choose whether to apply the filter in parallel using multi-threading.
- Compare Filters: Compares the original image with multiple filtered versions.
- Show Histogram: Displays histograms for the original and filtered images.
- Adjust Filter Parameter: Adjusts the parameter (kernel size) of the selected filter.
- Apply Adjustment: Applies the filter with the adjusted parameter.
- Save Filtered Images: Saves the filtered color and grayscale images in a 'filtered' folder.
- Progress Bar: Shows a progress bar during filter application.
- Message Label: Displays informative messages and errors.

"""

import cv2, os
import numpy as np
import concurrent.futures
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Scale, Button, Label, filedialog, messagebox, ttk

class ImageFilterApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Filter App")

        self.image = None
        self.image_path = None
        self.filter_choice = None
        self.resized_image = None

        self.filter_comparison_images = []

        self.apply_parallel_var = tk.BooleanVar(value=False)

        self.create_widgets()
    
    def create_widgets(self):
        # Load Image Button
        load_button = Button(self.master, text="Load Image", command=self.load_image)
        load_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Resize Image Button
        resize_button = Button(self.master, text="Resize Image", command=self.resize_image)
        resize_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        # Filter Type Entry
        filter_label = Label(self.master, text="Choose a filter (1: Mean, 2: Gaussian, 3: Median, 4: Custom):")
        filter_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.filter_choice_entry = tk.Entry(self.master)
        self.filter_choice_entry.grid(row=2, column=1, pady=5, padx=10, sticky="ew")
        
        # Checkbox for choosing parallel processing
        parallel_checkbox = tk.Checkbutton(self.master, text="Apply in Parallel", variable=self.apply_parallel_var)
        parallel_checkbox.grid(row=2, column=2, pady=5, padx=10, sticky="w")

        # Apply Filter Button
        apply_filter_button = Button(self.master, text="Apply Filter", command=self.apply_filter)
        apply_filter_button.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        # Compare Filters Button
        compare_filters_button = Button(self.master, text="Compare Filters", command=self.compare_filters)
        compare_filters_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        # Show Histogram Button
        self.hist_button = Button(self.master, text="Show Histogram", command=self.show_histograms)
        self.hist_button.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        #Adjust Filter Parameter Scale
        Label(self.master, text="Adjust Filter Parameter:").grid(row=5, column=0, pady=5, padx=10, sticky="w")
        self.param_scale = Scale(self.master, from_=1, to=15, orient=tk.HORIZONTAL, label="Kernel Size")
        self.param_scale.grid(row=5, column=1, pady=5, padx=10, sticky="ew")

        # Apply Adjusted Button
        apply_adjustment_button = Button(self.master, text="Apply Adjustment", command=self.adjust_parameter)
        apply_adjustment_button.grid(row=6, column=0, pady=10, padx=10, sticky="ew")

        # Save Image Button
        save_images_button = Button(self.master, text="Save Filtered Images", command=self.save_images)
        save_images_button.grid(row=6, column=1, pady=10, padx=10, sticky="ew")

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.master, mode='indeterminate')
        self.progress_bar.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Message Label
        self.message_label = Label(self.master, text="", fg='blue')
        self.message_label.grid(row=8, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

    def load_image(self):
        # Clear previous images
        self.clear_images()

        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.image_path = file_path
                self.image = cv2.imread(self.image_path)
                if self.image is not None:
                    self.display_image("Original Image", self.image)
                    self.update_message("Image loaded successfully.")
                else:
                    self.show_error("Error", "Invalid image file. Please select a valid image.")
            except Exception as e:
                self.show_error("Error", str(e))

    def resize_image(self):
        # Clear previous images
        self.clear_images()
        
        try:
            if self.image is not None:
                resize_factor = 0.5
                self.resized_image = cv2.resize(self.image, None, fx=resize_factor, fy=resize_factor)
                self.display_image("Resized Image", self.resized_image)
                self.update_message("Image resized successfully.")
            else:
                self.show_error("Error", "Load an image first.")
        except Exception as e:
            self.show_error("Error", str(e))

    def apply_filter(self):
        # Clear previous images
        self.clear_images()

        self.filter_choice = self.filter_choice_entry.get()

        if self.image is not None:
            try:
                self.star_progress_bar()
                if self.resized_image is not None:
                    self.apply_selected_filter(self.resized_image, parallel=self.apply_parallel_var.get())
                else:
                    self.apply_selected_filter(self.image, parallel=self.apply_parallel_var.get())
                self.update_message("Filter applied successfully.")
            except ValueError as ve:
                self.show_error("Error", str(ve))
            except Exception as e:
                self.show_error("Error", str(e))
            finally:
                self.stop_progress_bar()
        else:
            self.show_error("Error", "Load an image first.")
    
    def apply_selected_filter(self, selected_image, parallel=False):
        if self.filter_choice == '1':
            filter_class = MeanFilter
        elif self.filter_choice == '2':
            filter_class = GaussianFilter
        elif self.filter_choice == '3':
            filter_class = MedianFilter
        elif self.filter_choice == '4':
            filter_class = CustomFilter
        else:
            raise ValueError("Invalid filter choice. Using Mean FIlter.")

        if selected_image is not None:
            try:
                self.star_progress_bar()
                if parallel:
                    colr_filtered, _, _ = filter_class.apply_parallel(selected_image, 9)
                else:
                    colr_filtered, _, _ = filter_class.apply(selected_image, 9)

                self.filter_comparison_images.append(colr_filtered)
                self.color_filtered, self.gray_filtered, self.filter_type = colr_filtered, _, 'Custom'
                self.display_image(f"Filtered Image ({self.filter_type})", self.color_filtered)
            except Exception as e:
                self.show_error("Error", str(e))
        else:
            self.show_error("Error", "Load an image first.")

    def show_histograms(self):
        try:
            if self.image is not None and hasattr(self, 'color_filtered') and hasattr(self, 'gray_filtered'):
                histograms_window = tk.Toplevel(self.master)
                histograms_window.title("Histograms")

                original_hist = cv2.calcHist([cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
                filtered_hist = cv2.calcHist([cv2.cvtColor(self.color_filtered, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
                plt.figure(figsize=(10, 5))

                # Original Image Histogram
                plt.subplot(1, 2, 1)
                plt.title("Original Image Histogram")
                plt.xlabel("Pixel Intensity")
                plt.ylabel("Frequency")
                plt.plot(original_hist, color='black')

                # Filtered Image Histogram
                plt.subplot(1, 2, 2)
                plt.title("Filtered Image Histogram")
                plt.xlabel("Pixel Intensity")
                plt.ylabel("Frequency")
                plt.plot(filtered_hist, color='red')

                plt.tight_layout()
                # Embed the Matplotlib figure in Tkinter window
                canvas = FigureCanvasTkAgg(plt.gcf(), master=histograms_window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            else:
                self.show_error("Error", "Load and apply a filter to the image first.")
        except Exception as e:
            self.show_error("Error", str(e))

    def display_image(self, title, img):
        try:
            plt.figure(figsize=(5, 5))
            if len(img.shape) == 3:
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            else:
                plt.imshow(img, cmap='gray')
            plt.title(title)
            plt.axis('off')
            plt.pause(0.1)
        except Exception as e:
            self.show_error("Error", str(e))

    def adjust_parameter(self):
        # Clear previous images
        self.clear_images()

        if self.image is not None and hasattr(self, 'color_filtered') and hasattr(self, 'gray_filtered'):
            kernel_size = self.param_scale.get()
            try:
                self.star_progress_bar()

                # Resize the image for quicker adjustments
                resized_image = cv2.resize(self.image, None, fx=0.5, fy=0.5)

                if self.filter_type == 'Mean':
                    self.color_filtered, self.gray_filtered, _ = MeanFilter.apply(resized_image, kernel_size)
                elif self.filter_type == 'Gaussian':
                    self.color_filtered, self.gray_filtered, _ = GaussianFilter.apply(resized_image, kernel_size)
                elif self.filter_type == 'Median':
                    self.color_filtered, self.gray_filtered, _ = MedianFilter.apply(resized_image, kernel_size)
                elif self.filter_type == 'Custom':
                    self.color_filtered, self.gray_filtered, _ = CustomFilter.apply(resized_image, kernel_size)
                
                self.display_image(f"Filtered Image ({self.filter_type})", self.color_filtered)
                self.update_message("Parameter adjusted successfully.")
            except Exception as e:
                self.show_error("Error", str(e))
            finally:
                self.stop_progress_bar()
        else:
            self.show_error("Error", "Load and apply a filter to the image first.")

    def compare_filters(self):
        try:
            if self.image is not None and self.filter_comparison_images:
                images_to_display = [self.image] + self.filter_comparison_images
                titles = ["Original Image"] + [f"Filtered Image ({i+1})" for i in range(len(self.filter_comparison_images))]

                self.display_images_side_by_side(images_to_display, titles)
                self.update_message("Filter comparison displayed successfully.")
            else:
                self.show_error("Error", "Load an image and apply filters to compare.")
        except Exception as e:
            self.show_error("Error", str(e))

    def display_images_side_by_side(self, images, titles):
        try:
            num_images = len(images)
            plt.figure(figsize=(5 * num_images, 5))

            for i in range(num_images):
                plt.subplot(1, num_images, i+1)
                img = images[i]
                title = titles[i]

                if len(img.shape) == 3:
                    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                else:
                    plt.imshow(img, cmap='gray')

                plt.title(title)
                plt.axis('off')
            
            plt.show()
        except Exception as e:
            self.show_error("Error", str(e))

    def save_images(self):
        if self.image is not None and hasattr(self, 'color_filtered') and hasattr(self, 'gray_filtered'):
            image_name = os.path.splitext(os.path.basename(str(self.image_path)))[0]
            save_filtered_images(self.color_filtered, self.gray_filtered, image_name, self.filter_type)
            self.show_info("Success", "Filtered images saved successfully.")
        else:
            self.show_error("Error", "Load and apply a filter to the image first.")

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    def star_progress_bar(self):
        self.progress_bar.start(10)
        self.progress_bar_after_id = self.master.after(100, self.update_progress_bar)

    def update_progress_bar(self):
        self.progress_bar.step(1)
        if self.progress_bar['value'] < 100:
            self.progress_bar_after_id = self.master.after(100, self.update_progress_bar)

    def stop_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar['value'] = 0
        if self.progress_bar_after_id is not None:
            self.master.after_cancel(self.progress_bar_after_id)

    def clear_images(self):
        plt.close('all')

    def update_message(self, message):
        try:
            self.message_label.config(text=message)
        except tk.TclError:
            pass

        self.master.after(3000, lambda: self.clear_message())
    
    def clear_message(self):
        try:
            self.message_label.config(text="")
        except tk.TclError:
            pass

class MeanFilter:
    @staticmethod
    def apply(image, kernel_size):
        # Apply filter to the grayscale version
        gray_filtered = cv2.blur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (kernel_size, kernel_size))

        # Apply filter to the color version
        color_filtered = cv2.blur(image, (kernel_size, kernel_size))

        return color_filtered, gray_filtered, 'Mean'
    
    @staticmethod
    def apply_parallel(image, kernel_size):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_gray = executor.submit(cv2.blur, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (kernel_size, kernel_size))
            future_color = executor.submit(cv2.blur, image, (kernel_size, kernel_size))

            gray_filtered = future_gray.result()
            color_filtered = future_color.result()
        
        return color_filtered, gray_filtered, 'Mean'

class GaussianFilter:
    @staticmethod
    def apply(image, kernel_size):
        if kernel_size <= 0 or kernel_size % 2 == 0:
            raise ValueError("Invalid kernel size. Please use an odd positive integer.")
            
        # Apply filter to the grayscale version
        gray_filtered = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (kernel_size, kernel_size), 0)

        # Apply filter to the color version
        color_filtered = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

        return color_filtered, gray_filtered, 'Gaussian'

    
    @staticmethod
    def apply_parallel(image, kernel_size):
        if kernel_size <= 0 or kernel_size % 2 == 0:
            raise ValueError("Invalid kernel size. Please use an odd positive integer.")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_gray = executor.submit(cv2.GaussianBlur, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (kernel_size, kernel_size), 0)
            future_color = executor.submit(cv2.GaussianBlur, image, (kernel_size, kernel_size), 0)

            gray_filtered = future_gray.result()
            color_filtered = future_color.result()
        
        return color_filtered, gray_filtered, 'Gaussian'
        
class MedianFilter:
    @staticmethod
    def apply(image, kernel_size):
        if kernel_size <= 0 or kernel_size % 2 == 0:
            raise ValueError("Invalid kernel size. Please use an odd positive integer.")

        # Apply filter to the grayscale version
        gray_filtered = cv2.medianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), kernel_size)

        # Apply filter to the color version
        color_filtered = cv2.medianBlur(image, kernel_size)

        return color_filtered, gray_filtered, 'Median'
        
    @staticmethod
    def apply_parallel(image, kernel_size):
        try:
            if kernel_size <= 0 or kernel_size % 2 == 0:
                raise ValueError("Invalid kernel size. Please use an odd positive integer.")

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_gray = executor.submit(cv2.medianBlur, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), kernel_size)
                future_color = executor.submit(cv2.medianBlur, image, kernel_size)

                gray_filtered = future_gray.result()
                color_filtered = future_color.result()
            
            return color_filtered, gray_filtered, 'Median'
        except Exception as e:
            raise ValueError(f"Median filter failed: {str(e)}")
            
class CustomFilter:
    @staticmethod
    def apply(image, kernel_size):
        temp = []
        indexer = kernel_size // 2
        new_image = image.copy()
        nrow, ncol, _ = image.shape

        for i in range(nrow):
            for j in range(ncol):
                for k in range(i - indexer, i + indexer + 1):
                    for m in range(j - indexer, j + indexer + 1):
                        if 0 <= k < nrow and 0 <= m < ncol:
                            temp.append(image[k, m])
                temp = [x for x in temp if not np.array_equal(x, image[i, j])]
                if temp:
                    max_value = max(temp, key=lambda x: np.linalg.norm(x - image[i, j]))
                    min_value = min(temp, key=lambda x: np.linalg.norm(x - image[i, j]))
                    if np.array_equal(image[i, j], max_value):
                        new_image[i, j] = max_value
                    elif np.array_equal(image[i, j], min_value):
                        new_image[i, j] = min_value
                temp = []

        # Apply filter to the grayscale version
        gray_filtered = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

        return new_image, gray_filtered, 'Custom'

    @staticmethod
    def apply_parallel(image, kernel_size):
        indexer = kernel_size // 2
        new_image = image.copy()
        nrow, ncol, _ = image.shape

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(nrow):
                for j in range(ncol):
                    future = executor.submit(CustomFilter._process_pixel, image, new_image, i, j, indexer, nrow, ncol)
                    futures.append(future)
            
            # Wait for all threads to complete
            concurrent.futures.wait(futures)

        # Apply filter to the grayscale version
        gray_filtered = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

        return new_image, gray_filtered, 'Custom'
    
    @staticmethod
    def _process_pixel(image, new_image,i, j, indexer, nrow, ncol):
        temp = CustomFilter._collect_neighboring_pixels(image, i, j, indexer, nrow, ncol)

        if temp:
            max_value, min_value = CustomFilter._find_max_and_min_values(temp, image[i, j])

            if np.array_equal(image[i, j], max_value):
                new_image[i, j] = max_value
            elif np.array_equal(image[i, j], min_value):
                new_image[i, j] = min_value

    @staticmethod
    def _collect_neighboring_pixels(image, i, j, indexer, nrow, ncol):
        indices = np.indices((2*indexer+1, 2*indexer+1)) - indexer
        indices += np.array([i, j])[:, None, None]

        valid_indices = (indices[0] >= 0) & (indices[0] < nrow) & (indices[1] >= 0) & (indices[1] < ncol)

        return image[indices[0, valid_indices], indices[1, valid_indices]]

    @staticmethod
    def _find_max_and_min_values(pixel_list, current_pixel):
        norms = np.linalg.norm(pixel_list - current_pixel, axis=1)
        max_index = np.argmax(norms)
        min_index = np.argmin(norms)
        return pixel_list[max_index], pixel_list[min_index]


def save_filtered_images(filtered_color, filtered_gray, image_name, filter_type):
    try:
        # Check if filtered_color and filtered_gray are valid images
        if filtered_color is not None and filtered_gray is not None:
            filtered_folder = 'filtered'
            os.makedirs(filtered_folder, exist_ok=True)

            # Save filtered color image
            filtered_color_path = os.path.join(filtered_folder, f'{image_name}_color_{filter_type}.jpg')
            cv2.imwrite(filtered_color_path, filtered_color)

            # Save filtered grayscale image
            filtered_gray_path = os.path.join(filtered_folder, f'{image_name}_gray_{filter_type}.jpg')
            cv2.imwrite(filtered_gray_path, filtered_gray)

            print(f"Filtered images saved in '{filtered_folder}' folder.")
        else:
            print("Filtered images are not valid. Unable to save.")
    except Exception as e:
        print(f"An error occurred while saving filtered images: {str(e)}")

def main():
    try:
        root = tk.Tk()
        app = ImageFilterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()