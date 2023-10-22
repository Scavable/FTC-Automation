import tkinter as tk

class ResetWindow:
    def __init__(self):
        self.y = None
        self.x = None
        self.h = 0
        self.w = 0
        self.root = tk.Tk()

        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()

    def size(self, w, h):
        self.w = w
        self.h = h

    def position_center(self):
        self.x = (self.ws / 2) - (self.w / 2)
        self.y = (self.hs / 2) - (self.h / 2)

        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
    def position(self, x, y):
        self.x = (self.ws / 2) - (self.w / 2)
        self.y = (self.hs / 2) - (self.h / 2)

        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def run(self):
        self.root.mainloop()