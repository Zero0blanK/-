import json
import os
import shutil
from tkinter import END, filedialog, messagebox
import customtkinter
import pygame
from segmentedbutton_frame import Segmentedbutton_Frame
from music_player_frame import Music_Player_Frame
from musicPlaylist_frame import MusicPlaylist_Frame


class User_App(customtkinter.CTk):               
    def __init__(self):
        super().__init__()  
        self.title('Modern User Interface')
        self.geometry('800x500')
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=2)
        self.protocol("WM_DELETE_WINDOW", self.stop_music)
        
        add_button = customtkinter.CTkButton(self, text='Add Music', font=("Times New Roman", 20), height=35, width=150, corner_radius=60, command=self.open_folder)
        add_button.grid(row=1 , column=0)
        
        self.musicplayer_frame = Music_Player_Frame(self)
        self.musicplayer_frame.grid(row=0, column=3, padx=(0, 10), pady=(10, 0), ipady=400, ipadx=42)  
        self.musicplayer_frame.song_list = self.musicplayer_frame.song_list  
        
        self.musicPlaylist_frame = MusicPlaylist_Frame(self, self.musicplayer_frame)
        self.musicPlaylist_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky='nwse', ipadx=38)
        
        self.menu_frame = Segmentedbutton_Frame(self, 'Library', values=['General','Goddess Nihon', 'Hakdog', 'Liked'], command=self.change_library)
        self.menu_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky='nwse')
        
        
        self.song_library = []  
    
    def stop_music(self):
        pygame.mixer.music.stop()  # Stop music playback
        self.destroy()  
        
    def open_folder(self):
        while True:
            # Allow the user to select individual music files and album covers
            music_files = filedialog.askopenfilenames(title="Select Music Files", filetypes=[("MP3 Files", "*.mp3")])
            if not music_files:
                break
            
            music_exists = False
            for music_file in music_files:
                music_name = os.path.basename(music_file)
                music_path = os.path.join(os.getcwd(), 'music', music_name)

                if os.path.exists(music_path):
                    music_exists = True
                    break
            
            if music_exists:
                messagebox.showinfo("Duplicate Music", "One or more selected music files already exist in the library. Please select different music files.")
            else:
                for music_file in music_files:
                    music_name = os.path.basename(music_file)
                    music_path = os.path.join(os.getcwd(), 'music', music_name)
                    # Copy the music file to the music directory
                    shutil.copy2(music_file, music_path)
                    # Get the album cover path and name
                    album_cover_file = filedialog.askopenfilename(title="Select Album Cover", filetypes=[("Image Files", "*.jpg;*.png")])
                    if album_cover_file:
                        album_cover_name = music_name.split('.')[0] + os.path.splitext(album_cover_file)[1]
                        album_cover_path = os.path.join(os.getcwd(), 'album_covers', album_cover_name)
                        # Copy the album cover to the album_covers directory
                        shutil.copy2(album_cover_file, album_cover_path)
                    # Update the playlist
                    self.musicPlaylist_frame.playlist.insert(END, music_name)
                    # Add the library name to the song_library list
                    self.song_library.append(self.menu_frame.variable.get())
                    # Add the music file to the song list
                    self.musicplayer_frame.song_list.append(music_path)
                    self.musicPlaylist_frame.playlist.update_idletasks()  # Force update of the playlist widget
                break

                        
    def change_library(self, library_name):
        self.musicPlaylist_frame.update_playlist(library_name, self.song_library)
        
        
if __name__ == '__main__':
    app = User_App()
    app.mainloop()