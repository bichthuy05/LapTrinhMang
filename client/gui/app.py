# app.py
import tkinter as tk
import os
from gui.buttons import ChoiceButton
from gui.animations import LoadingAnimation, flash_background
from network.client_net import ClientNetwork  

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rock Paper Scissors")
        self.window.geometry("600x400")
        self.window.config(bg="white")

        self.label = tk.Label(self.window, text="Đang chờ đối thủ", font=("Arial", 16))
        self.label.pack(pady=10)

        self.loader = LoadingAnimation(self.label)
        self.loader.start()

        self.net = ClientNetwork(self.update_status)
        self.load_images()  # ✅ Load ảnh
        self.create_image_display()  # ✅ Thêm label hiển thị ảnh
        self.create_buttons()

    def load_images(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.images = {
            'rock': tk.PhotoImage(file=os.path.join(base_path, "rock.png")),
            'paper': tk.PhotoImage(file=os.path.join(base_path, "paper.png")),
            'scissors': tk.PhotoImage(file=os.path.join(base_path, "scissors.png"))
        }

    def create_image_display(self):
        self.image_label = tk.Label(self.window, bg="white")
        self.image_label.pack(pady=10)

    def create_buttons(self):
        frame = tk.Frame(self.window, bg="white")
        frame.pack(pady=10)

        for choice in ['rock', 'paper', 'scissors']:
            btn = ChoiceButton(frame, choice, self.on_choice)
            btn.pack(side=tk.LEFT, padx=20)

    def on_choice(self, choice):
        self.label.config(text=f"Đã chọn: {choice}")
        self.net.send_choice(choice)

        # ✅ Hiển thị ảnh tương ứng
        self.image_label.config(image=self.images[choice])
        self.image_label.image = self.images[choice]  # giữ tham chiếu

    def update_status(self, status_text):
        self.label.config(text=status_text)

        if "Đối thủ" in status_text or "Thắng" in status_text or "Thua" in status_text:
            self.loader.stop()

        if "Thắng" in status_text:
            flash_background(self.window, "green")
        elif "Thua" in status_text:
            flash_background(self.window, "red")

    def run(self):
        self.window.mainloop()