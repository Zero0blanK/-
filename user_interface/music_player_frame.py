import os
import customtkinter
from tkinter import *
import pygame
from threading import *
from PIL import Image, ImageTk
import time


class Music_Player_Frame(customtkinter.CTkFrame):
    def __init__(self, master, song_list=[]):
        super().__init__(master)
        pygame.mixer.init()
        
        self.song_list = song_list
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        album_covers_directory = os.path.join(parent_directory, 'album_covers')
        self.song_cover_path = album_covers_directory
        
        self.song_cover_files = []
        self.n = 0

        
        self.play_button = customtkinter.CTkButton(master=self, text='Play', width=100, height=40, command= self.play_music)
        self.play_button.place(x=140, y=370, anchor='center')

        skip_f = customtkinter.CTkButton(self, text='>', width=30, height=40, command= self.skip_forward)
        skip_f.place(x=209, y=370, anchor='center')
        
        skip_b = customtkinter.CTkButton(self, text='<', width=30, height=40, command= self.skip_back)
        skip_b.place(x=71, y=370, anchor='center')
        
        volume_slider = customtkinter.CTkSlider(self, from_=0, to=1, width=210, command=self.volume)
        volume_slider.place(x=141, y=410, anchor='center')
        
        self.music_bar = customtkinter.CTkProgressBar(self, width=250)
        self.music_bar.place(x=142, y=330, anchor='center')
        
        self.progress_thread = None
        self.playing = False
        self.next = False
        self.get_albumcover()
        
    def get_albumcover(self):
        self.song_cover_files.clear()

        for album in os.listdir(self.song_cover_path):
            if album.endswith(('.jpg', '.png')):
                self.song_cover_files.append(os.path.join(self.song_cover_path, album))
                
        if self.song_cover_files:        
            self.image1 = Image.open(self.song_cover_files[self.n])
            self.image2 = self.image1.resize((250,250))
            self.load = ImageTk.PhotoImage(self.image2)
            self.label1 = Label(self, image=self.load)
            self.label1.place(x=15, y=15)
            
        if self.song_list:
            self.stripped_string = os.path.basename(self.song_list[self.n][36:-4])
            if hasattr(self, 'song_name_label'): # Check if there's an existing label
                self.song_name_label.destroy()

            if not self.next: #Create a new label for the next song
                self.song_name_label = Label(self, text=self.stripped_string, bg='#222222', fg='white', font=20)
                self.song_name_label.place(x=135, y=290, anchor='center')
    
    def progress_bar(self):
        song_length = pygame.mixer.Sound(self.song_list[self.n]).get_length()
        while pygame.mixer.music.get_busy():
            if self.playing:
                current_time = pygame.mixer.music.get_pos() / 1000
                self.music_bar.set(current_time / song_length)
                self.music_bar.update() #force update in progress bar in the main thread
            time.sleep(0.3)
    
    def threading(self):
        if self.progress_thread and self.progress_thread.is_alive():
            return
        self.progress_thread = Thread(target=self.progress_bar)
        self.progress_thread.start()
    
    def play_music(self, index=None, library_name='General'):
        if index is not None:
            self.n = index

        self.threading()
        self.get_albumcover()
        
        pygame.mixer.music.load(self.song_list[self.n])
        pygame.mixer.music.play(loops=1)
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button.configure(text='Play')
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.play_button.configure(text='Pause')
            self.playing = True

    def skip_forward(self):
        self.playing = False
        self.next = False
        self.n = (self.n + 1) % len(self.song_list) #Ensure it loops around the song list
        self.play_music()
        
    def skip_back(self):
        self.playing = False
        self.next = False
        self.n = (self.n - 1) % len(self.song_list)
        self.play_music()
        
    def volume(self, value):
        self.value = float(value)
        pygame.mixer.music.set_volume(self.value)
        
        