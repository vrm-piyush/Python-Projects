"""
Text to Speech (TTS) Conversion Program.

Input:
- URL of an article to be converted to speech.
- Optional: Speech speed, volume, and output file format.

Output:
- Audio file containing the speech rendition of the article.
- Playback of the generated audio file.

Features:
- Utilizes the 'newspaper' library to extract and process article text from the provided URL.
- Uses the 'gtts' library to convert the article text to speech.
- Plays the generated audio file.
- Adjustable speech speed and volume controls.
- Option to save the audio file in different formats.
- Logging of successful conversions and errors.
- Prompt to delete the generated audio file after playback.
- Keyboard shortcut to close the application (Ctrl + Q).
- Error handling for invalid URLs and unexpected errors.

"""

import os
import pyttsx3
import logging
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from pynput import keyboard
from newspaper import Article, ArticleException

class ArticleToSpeechConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Article to Speech Converter")

        self.url_label = ttk.Label(self, text="Article URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Speed Slider
        self.speed_label = ttk.Label(self, text="Speech Speed:")
        self.speed_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.speed_scale = ttk.Scale(self, from_=50, to=300, length=200, orient="horizontal")
        self.speed_scale.set(150)  # Default speed value
        self.speed_scale.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Volume Slider
        self.volume_label = ttk.Label(self, text="Volume:")
        self.volume_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.volume_scale = ttk.Scale(self, from_=0, to=100, length=200, orient="horizontal")
        self.volume_scale.set(100)  # Default volume value
        self.volume_scale.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.output_format_label = ttk.Label(self, text="Output File Format (e.g., 'mp3', 'wav'):")
        self.output_format_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.output_format_entry = ttk.Entry(self, width=10)
        self.output_format_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.convert_button = ttk.Button(self, text="Convert to Speech", command=self.convert_to_speech)
        self.convert_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Set up logging
        logging.basicConfig(filename="app.log", level=logging.INFO)

        self.status_label = ttk.Label(self, text="")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)

        self.bind("<Control-q>", self.quit_application)

    def convert_to_speech(self):
        try:
            article_url  = self.url_entry.get()
            speed = self.speed_scale.get()
            volume = self.volume_scale.get() / 100
            output_format = self.output_format_entry.get().lower()
            
            article = Article(article_url)
            article.download()
            article.parse()
            article.nlp()

            mytext = article.text

            # Initialize the text-to-speech engine
            engine = pyttsx3.init()

            # Set customization parameters
            engine.setProperty("rate", speed)
            engine.setProperty("volume", volume)

            # Create an 'audio' directory if it doesn't exist
            audio_folder = "audio"
            if not os.path.exists(audio_folder):
                os.makedirs(audio_folder)

            # Generate file name based on the article title within the 'audio' directory
            file_name = os.path.join(audio_folder, article.title.replace(" ", "_") + f".{output_format}")

            # Save the audio file
            engine.save_to_file(mytext, file_name)
            engine.runAndWait()

            self.status_label["text"] = f"Audio file '{file_name}' created successfully.\nPlaying audio...\n"
            logging.info(f"{datetime.now()} - Audio file '{file_name}' created successfully. Playing audio...")

            # Log the successful conversion
            logging.info(f"{datetime.now()} - Article converted successfully: {article_url}")

            # USe subprocess to play the audio file
            subprocess.Popen(['start', file_name], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

            self.after(5000, self.show_delete_option, file_name)

        except ArticleException as ae:
            self.status_label["text"] = f"Article Exception: {ae}"
            logging.error(f"{datetime.now()} - Article Exception: {ae}")
        except Exception as e:
            self.status_label["text"] = f"An unexpected error occurred: {e}"
            logging.error(f"{datetime.now()} - An unexpected error occurred: {e}")

    def show_delete_option(self, file_name):
        delete_option = messagebox.askyesno("Delete Audio File", f"Do you want to delete the audio file '{file_name}'?")
        if delete_option:
            os.remove(file_name)
            self.status_label["text"] += f"Audio file '{file_name}' deleted successfully."
            logging.info(f"{datetime.now()} - Audio file '{file_name}' deleted successfully.")

    def quit_application(self, event):
        logging.info(f"{datetime.now()} - Application closed by user.")
        self.destroy()


if __name__ == "__main__":
   app = ArticleToSpeechConverter()
   app.mainloop()