"""
Main application class for FocusSense.
Handles window, navigation, and screen management with sidebar UI.
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

        self.current_subject = "General"
        self.current_screen = None  # track active screen

        # -------- MAIN LAYOUT --------
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # -------- SIDEBAR --------
        self.sidebar = tk.Frame(main_frame, width=150, bg="#222")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # lock width

        # -------- CONTENT AREA --------
        self.container = tk.Frame(main_frame)
        self.container.pack(side="right", fill="both", expand=True)

        # allow resizing
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # -------- SIDEBAR BUTTONS --------
        self.buttons = {}

        btn_style = {
            "fg": "white",
            "bg": "#222",
            "activebackground": "#444",
            "bd": 0,
            "font": ("Helvetica", 12),
            "anchor": "w",
            "padx": 10
        }

        def add_button(name, screen):
            btn = tk.Button(
                self.sidebar,
                text=name,
                command=lambda: self.show(screen),
                **btn_style
            )
            btn.pack(fill="x", pady=5)
            self.buttons[screen] = btn

        add_button("Home", HomeScreen)
        add_button("Focus", FocusModeScreen)
        add_button("Stats", StatsScreen)

        # -------- SCREENS --------
        self.frames = {}

        for Screen in (HomeScreen, FocusModeScreen, StatsScreen):
            frame = Screen(self.container, self)
            self.frames[Screen] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(HomeScreen)

    def show(self, screen):
        # raise frame
        self.frames[screen].tkraise()
        self.current_screen = screen

        # highlight active button
        for scr, btn in self.buttons.items():
            if scr == screen:
                btn.config(bg="#444")
            else:
                btn.config(bg="#222")

    def update_camera(self, frame):
        self.frames[FocusModeScreen].update_camera(frame)

    def update_score(self, score):
        self.frames[FocusModeScreen].update_score(score)

    def run(self):
        self.root.mainloop()


