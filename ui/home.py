import tkinter as tk


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="FocusSense", font=("Helvetica", 24)).pack(pady=20)

        tk.Button(
            self,
            text="Start Focus Mode",
            command=lambda: controller.show(controller.frames.keys().__iter__().__next__().__class__)
        ).pack(pady=10)

