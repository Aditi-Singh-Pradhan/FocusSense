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

        self.current_subject = "General"   # default value

        # -------- MAIN LAYOUT --------
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # -------- SIDEBAR --------
        sidebar = tk.Frame(main_frame, width=150, bg="#222")
        sidebar.pack(side="left", fill="y")

        # -------- CONTENT AREA --------
        self.container = tk.Frame(main_frame)
        self.container.pack(side="right", fill="both", expand=True)

        # -------- SIDEBAR BUTTONS --------
        btn_style = {
            "fg": "white",
            "bg": "#222",
            "activebackground": "#444",
            "bd": 0,
            "font": ("Helvetica", 12),
            "anchor": "w",
            "padx": 10
        }

        tk.Button(
            sidebar,
            text="Home",
            command=lambda: self.show(HomeScreen),
            **btn_style
        ).pack(fill="x", pady=5)

        tk.Button(
            sidebar,
            text="Focus",
            command=lambda: self.show(FocusModeScreen),
            **btn_style
        ).pack(fill="x", pady=5)

        tk.Button(
            sidebar,
            text="Stats",
            command=lambda: self.show(StatsScreen),
            **btn_style
        ).pack(fill="x", pady=5)

        # -------- SCREENS --------
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

