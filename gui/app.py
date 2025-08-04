# app.py
import tkinter as tk
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
        self.label.pack(pady=20)

        self.loader = LoadingAnimation(self.label)
        self.loader.start()

        self.net = ClientNetwork(self.update_status)
        self.create_buttons()

    def create_buttons(self):
        frame = tk.Frame(self.window, bg="white")
        frame.pack(pady=30)

        for choice in ['rock', 'paper', 'scissors']:
            btn = ChoiceButton(frame, choice, self.on_choice)
            btn.pack(side=tk.LEFT, padx=20)

    def on_choice(self, choice):
        self.label.config(text=f"Đã chọn: {choice}")
        self.net.send_choice(choice)

    def update_status(self, status_text):
        self.label.config(text=status_text)

        # Tắt loading nếu không còn chờ
        if "Đối thủ" in status_text or "Thắng" in status_text or "Thua" in status_text:
            self.loader.stop()

        # Hiệu ứng kết quả
        if "Thắng" in status_text:
            flash_background(self.window, "green")
        elif "Thua" in status_text:
            flash_background(self.window, "red")

    def run(self):
        self.window.mainloop()
