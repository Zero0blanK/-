import os
from tkinter import END, filedialog
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
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs=os.listdir(path)
            if songs:
                self.musicPlaylist_frame.playlist.delete(0, END)
                for song in songs:
                    if song.endswith('.mp3'):
                        full_path = os.path.join(path, song)
                        # Append the song to the song list
                        self.musicplayer_frame.song_list.append(full_path)
                        # Append the library name separately
                        self.song_library.append(self.menu_frame.variable.get())
                        self.musicPlaylist_frame.playlist.insert(END, song)
                        self.musicPlaylist_frame.playlist.update_idletasks()  # Force update of the playlist widget

                        
    def change_library(self, library_name):
        self.musicPlaylist_frame.update_playlist(library_name, self.song_library)
        
if __name__ == '__main__':
    app = User_App()
    app.mainloop()