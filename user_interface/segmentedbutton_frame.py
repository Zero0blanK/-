from PIL import Image
import customtkinter

class Segmentedbutton_Frame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.values = values
        self.title = title
        self.menu = []
        self.variable = customtkinter.StringVar(value=values[0])
        
        #add another library for music function is not yet added
        add_button = customtkinter.CTkImage(light_image=Image.open('C:/Users/April Bords/OneDrive/Desktop/Programming/Practical Coding/Python/MusicPlayer/img/add.png'))
        
        self.menu_title = customtkinter.CTkLabel(self, text=self.title, corner_radius=5, font=('Times New Roman', 20))
        self.menu_title.grid(column=0, row=0, pady=(10, 10), padx=(30,0), sticky='nwe')
        
        self.image_label = customtkinter.CTkButton(self.menu_title, text="", image=add_button, width=8, fg_color='transparent', anchor='w')
        self.image_label.grid(column=1, row=0, pady=(0, 5), padx=(0,10), sticky='we')
        
        for i in range(len(self.values)):
            segmented_button = customtkinter.CTkSegmentedButton(self, values=[self.values[i]])
            segmented_button.grid(column=0, row=i+1, pady=(5,0), sticky='wne', ipadx=40, ipady=3)
            self.menu.append(segmented_button)
            segmented_button.configure(variable=self.variable)