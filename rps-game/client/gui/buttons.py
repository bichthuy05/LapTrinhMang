import os
from pathlib import Path
from tkinter import Button
from PIL import Image, ImageTk

class ChoiceButton(Button):
    def __init__(self, master, choice, command):
        # Sử dụng đường dẫn tương đối an toàn
        base_path = Path(__file__).parent.parent.parent / "client" / "assets"
        img_path = base_path / f"{choice}.png"
        
        # Fallback nếu không tìm thấy ảnh
        if not img_path.exists():
            self.photo = None
        else:
            img = Image.open(img_path).resize((100, 100))
            self.photo = ImageTk.PhotoImage(img)

        super().__init__(master, image=self.photo, command=lambda: self._on_click(choice))
        self._callback = command

    def _on_click(self, choice):
        if self.photo:  # Chỉ gọi callback nếu ảnh tồn tại
            self._callback(choice)