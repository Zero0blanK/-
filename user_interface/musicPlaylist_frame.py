import os
import customtkinter
from tkinter import *

import pygame

from music_player_frame import Music_Player_Frame

class MusicPlaylist_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, musicplayer_frame):
        super().__init__(master)
        
        self.musicplayer_frame = musicplayer_frame
        
        music_frame = customtkinter.CTkScrollableFrame(self, width=500, height=250)
        music_frame.grid(row=1, column=0)

        self.playlist = Listbox(self, width=100, font=("Times New Roman", 12))
        self.playlist.grid(row=1, column=0)
        self.playlist.bind('<Double-Button-1>', self.play_selected_song)
        
        self.selected_library = 'General' #default playlist library

    def play_selected_song(self, event):
        selected_index = self.playlist.curselection()
        if selected_index:
            index = int(selected_index[0])
            if self.musicplayer_frame.playing:
                pygame.mixer.music.unpause()  # Stop the currently playing music
            # Retrieve the library name for the selected song
            selected_song = self.musicplayer_frame.song_list[index]
            library_name = selected_song[1]
            self.musicplayer_frame.play_music(index, library_name)
    
    def update_playlist(self, library_name, song_library):
        self.selected_library = library_name
        self.playlist.delete(0, END)
        for i, song in enumerate(self.musicplayer_frame.song_list):
            song_name = os.path.basename(song)
            song_library_name = song_library[i]
            if library_name == 'General' or song_library_name == library_name:
                self.playlist.insert(END, song_name)