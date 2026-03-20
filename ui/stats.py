import tkinter as tk

from ui.home import HomeScreen 

class StatsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Statistics", font=("Helvetica", 20)).pack(pady=10)

        # Placeholder for stats content
        tk.Label(self, text="Your focus statistics will appear here.", font=("Helvetica", 14)).pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show(HomeScreen)).pack(pady=10)