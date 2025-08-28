import tkinter as tk
from tkinter import simpledialog, messagebox

root = tk.Tk()
root.withdraw()
name = simpledialog.askstring("Test", "Nhập tên của bạn:")
print("Bạn đã nhập:", name)
root.destroy()
