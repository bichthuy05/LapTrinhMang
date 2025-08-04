
import tkinter as tk
from PIL import Image, ImageTk

class ChoiceButton(tk.Button):
    def __init__(self, master, choice, command):
        self.choice = choice
        img_path = f"assets/{choice}.png"
        img = Image.open(img_path).resize((100, 100))
        self.photo = ImageTk.PhotoImage(img)

        super().__init__(master, image=self.photo, command=self.on_click)
        self._callback = command

    def on_click(self):
        self._callback(self.choice)
