import Tkinter as tk
#from config import gui_options


class GUIProcess():
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.frame = tk.Frame(self.master, *args, **kwargs)
        self.frame.grid()

    def quit(self):
        pass
