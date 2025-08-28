import tkinter as tk
from tkinter import simpledialog, messagebox

def ask_username():
    root = tk.Tk()
    root.withdraw()  # ẩn cửa sổ chính
    user_name = simpledialog.askstring("Nhập thông tin", "Hãy nhập tên của bạn:")
    if user_name:
        messagebox.showinfo("Chào bạn", f"Xin chào, {user_name}!")
    else:
        messagebox.showwarning("Cảnh báo", "Bạn chưa nhập tên!")
    root.destroy()
    return user_name
