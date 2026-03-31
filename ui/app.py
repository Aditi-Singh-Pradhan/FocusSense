"""
Contains the main application class that initializes the Tkinter window and manages screen transitions.

"""


import tkinter as tk

from ui.home import HomeScreen
from ui.focusmode import FocusModeScreen
from ui.stats import StatsScreen



class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FocusSense")
        self.root.geometry("900x600")

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        self.current_subject = "General"   # ✅ default value

        # Create menu bar
        menubar = tk.Menu(self.root) 

        menu = tk.Menu(menubar, tearoff=0) 
        menu.add_command(label="Home", command=lambda: self.show(HomeScreen)) 
        menu.add_command(label="Stats", command=lambda: self.show(StatsScreen)) 
        menubar.add_cascade(label="Menu", menu=menu)

        self.root.config(menu=menubar)

        self.frames = {}

        for Screen in (HomeScreen, FocusModeScreen, StatsScreen):
            frame = Screen(self.container, self)
            self.frames[Screen] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(HomeScreen)

    def show(self, screen):
        self.frames[screen].tkraise()

    def update_camera(self, frame):

        self.frames[FocusModeScreen].update_camera(frame)

    def update_score(self, score):
        self.frames[FocusModeScreen].update_score(score)

    def run(self):
        self.root.mainloop()
