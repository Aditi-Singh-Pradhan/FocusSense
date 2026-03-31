import tkinter as tk
from ui.stats import StatsScreen

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="FocusSense", font=("Helvetica", 24)).pack(pady=20)

        # View stats button
        tk.Button(
            self,
            text="View Stats",
            command=lambda: controller.show(StatsScreen)
        ).pack(pady=10)

        # SUBJECT SELECTOR 
        tk.Label(self, text="What are you studying?").pack()

        self.subject_var = tk.StringVar()
        self.subject_var.set("Math")

        subjects = ["Math", "Chem", "Physics", "Coding"]

        tk.OptionMenu(self, self.subject_var, *subjects).pack(pady=10)

        tk.Button(
            self,
            text="Start Focus Mode",
            command=self.start_focus
        ).pack(pady=10)

    def start_focus(self):
        subject = self.subject_var.get()
        print("Selected subject:", subject)

        self.controller.current_subject = subject  # 🔥 STORE GLOBALLY

        from ui.focusmode import FocusModeScreen
        self.controller.show(FocusModeScreen)

