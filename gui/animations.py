# animations.py

class LoadingAnimation:
    def __init__(self, label):
        self.label = label
        self.frames = ["", ".", "..", "..."]
        self.index = 0
        self.running = False

    def start(self):
        self.running = True
        self.animate()

    def stop(self):
        self.running = False

    def animate(self):
        if not self.running:
            return
        self.label.config(text="Đang chờ đối thủ" + self.frames[self.index])
        self.index = (self.index + 1) % len(self.frames)
        self.label.after(500, self.animate)

def flash_background(window, color, times=6, delay=200):
    def toggle(i):
        if i <= 0:
            window.config(bg="white")
            return
        current = window.cget("bg")
        new_color = color if current == "white" else "white"
        window.config(bg=new_color)
        window.after(delay, toggle, i - 1)
    toggle(times)
