import customtkinter
from tkinter import *

from music_player_frame import Music_Player_Frame

class MusicPlaylist_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.musicplayer_frame = Music_Player_Frame(self)
        
        music_frame = customtkinter.CTkScrollableFrame(self, width=500, height=250)
        music_frame.grid(row=1, column=0)

        self.playlist = Listbox(self, width=100, font=("Times New Roman", 10))
        self.playlist.grid(row=1, column=0)
        self.playlist.bind('<Double-Button-1>', self.play_selected_song)

    def play_selected_song(self, event):
        selected_index = self.playlist.curselection()
        if selected_index:
            index = selected_index[0]
            self.musicplayer_frame.play_music(index)