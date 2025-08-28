from client.gui.app import App
from shared.protocol import Protocol
import tkinter as tk

def main():
    print("🟢 Đang khởi động ứng dụng...")
    app = App()
    app.run()

if __name__ == "__main__":
    main()
