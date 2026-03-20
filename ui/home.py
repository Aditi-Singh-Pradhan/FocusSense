import tkinter as tk
from ui.focusmode import FocusModeScreen



class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="FocusSense", font=("Helvetica", 24)).pack(pady=20)

        tk.Button(
            self,
            text="Start Focus Mode",
            command=lambda: controller.show(FocusModeScreen)
        ).pack(pady=10)

