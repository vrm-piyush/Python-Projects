"""
Music Player GUI Program.

Input:
- No input required from the user.

Output:
- Displays a music player GUI allowing users to play, stop, pause, and resume songs.

Features:
- Initializes and configures a music player GUI window using Tkinter.
- Prompts the user to select a directory containing music files.
- Loads songs from the selected directory.
- Creates a playlist widget to display the list of songs.
- Utilizes pygame mixer for playing audio files.
- Implements functions for playing, stopping, pausing, and resuming songs.
- Customizes GUI components, styles, and button icons.

"""

import pygame
import tkinter as tkr
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.ttk import Button as ttkButton
import os

def initialize_music_player() -> tkr.Tk:
    """
    Initialize and configure the music player GUI window.
    
    Returns:
    - tkr.Tk: Initialized music player GUI window.
    """
    music_player = tkr.Tk()
    music_player.title("Music Player")
    music_player.geometry("450x450")
    music_player.configure(bg='#CF393B')  # Set background color
    return music_player

def load_songs(directory: str) -> list:
    """
    Load songs from the specified directory.
    
    Args:
    - directory (str): Directory path containing music files.
    
    Returns:
    - list: List of song filenames.
    """
    return os.listdir(directory)

def create_playlist(music_player: tkr.Tk, song_list: list) -> tkr.Listbox:
    """
    Create a playlist based on the provided list of songs.
    
    Args:
    - music_player (tkr.Tk): Music player GUI window.
    - song_list (list): List of songs to populate in the playlist.
    
    Returns:
    - tkr.Listbox: Playlist widget containing the song list.
    """
    play_list = tkr.Listbox(music_player, font=("Arial", 12), bg='#ecd444', fg='black', 
                            selectbackground='gray', selectforeground='black', selectmode=tkr.SINGLE)
    for item in song_list:
        play_list.insert(tkr.END, item)
    return play_list

# Define functions for music player controls.
def play_song() -> None:
    """Play the selected song."""
    song = play_list.get(tkr.ACTIVE)
    pygame.mixer.music.load(song)
    var.set(song)
    pygame.mixer.music.play()

def stop_song() -> None:
    """Stop the currently playing song."""
    pygame.mixer.music.stop()

def pause_song() -> None:
    """Pause the currently playing song."""
    pygame.mixer.music.pause()

def resume_song() -> None:
    """Resume the paused song."""
    pygame.mixer.music.unpause()

if __name__ == '__main__':
    # Initialize the music player GUI.
    music_player = initialize_music_player()

    # Prompt user to select the directory containing music files.
    directory = askdirectory()
    os.chdir(directory)  # Set current directory to selected directory.
    
    # Load songs from the selected directory.
    song_list = load_songs(directory)

    # Create the playlist.
    play_list = create_playlist(music_player, song_list)

    # Initialize pygame mixer.
    pygame.init()
    pygame.mixer.init()

    # Create GUI components and styles.
    var = tkr.StringVar()
    song_title = tkr.Label(music_player, font=("Gotham", 14, "bold"), bg='#CF393B', fg='white', textvariable=var)
    
    # Load icon images for buttons.
    play_icon = tkr.PhotoImage(file='C:/Users/ashok/source/Python 60 Projects/18. MusicPlayerGUI/MusicPlayerIcons/play_icon.png')
    stop_icon = tkr.PhotoImage(file='C:/Users/ashok/source/Python 60 Projects/18. MusicPlayerGUI/MusicPlayerIcons/stop_icon.png')
    pause_icon = tkr.PhotoImage(file='C:/Users/ashok/source/Python 60 Projects/18. MusicPlayerGUI/MusicPlayerIcons/pause_icon.png')
    resume_icon = tkr.PhotoImage(file='C:/Users/ashok/source/Python 60 Projects/18. MusicPlayerGUI/MusicPlayerIcons/resume_icon.png')

    # Create buttons with icons and text
    Button1 = ttkButton(music_player, text="PLAY", width=20, image=play_icon, compound=tkr.TOP, command=play_song)
    Button1.configure(style='Green.TButton')
    Button2 = ttkButton(music_player, text="STOP", width=20, image=stop_icon, compound=tkr.TOP, command=stop_song)
    Button2.configure(style='Blue.TButton')
    Button3 = ttkButton(music_player, text="PAUSE", width=20, image=pause_icon, compound=tkr.TOP, command=pause_song)
    Button3.configure(style='Pink.TButton')
    Button4 = ttkButton(music_player, text="RESUME", width=20, image=resume_icon, compound=tkr.TOP, command=resume_song)
    Button4.configure(style='Yellow.TButton')
    
    # Create custom styles for colored buttons
    style=ttk.Style(music_player)
    style.configure('Pink.TButton', foreground='black', background='pink')
    style.configure('Blue.TButton', foreground='black', background='blue')
    style.configure('Green.TButton', foreground='black', background='green')
    style.configure('Yellow.TButton', foreground='black', background='yellow')

    # Pack GUI components with increased gaps between buttons
    song_title.pack(pady=20)
    Button1.pack(side=tkr.TOP, padx=5, pady=5)
    Button2.pack(side=tkr.TOP, padx=5, pady=5)
    Button3.pack(side=tkr.TOP, padx=5, pady=5)
    Button4.pack(side=tkr.TOP, padx=5, pady=5)
    play_list.pack(fill="both", expand=1, padx=20, pady=10)


    # Start the music player GUI event loop.
    music_player.mainloop()