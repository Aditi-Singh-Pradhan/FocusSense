"""
Focus Mode screen for FocusSense.

Displays:
- Focus score
- System messages
- Task checklist
- Timer (placeholder)
- Camera placeholder
"""

import tkinter as tk
from PIL import Image, ImageTk 
import cv2


class FocusModeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------- TITLE ----------
        tk.Label(self, text="Focus Mode", font=("Helvetica", 20)).pack(pady=10)

        # ---------- TOP FRAME (Camera + Timer) ----------
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        # Camera placeholder
        self.camera_label = tk.Label(
            top_frame,
            text="Camera Feed",
            bg="black",
        )
        self.camera_label.grid(row=0, column=0, padx=10)

        # Timer placeholder
        self.timer_label = tk.Label(
            top_frame,
            text="Timer: 00:00",
            font=("Helvetica", 14)
        )
        self.timer_label.grid(row=0, column=1, padx=10)

        # ---------- FOCUS SCORE ----------
        self.score_label = tk.Label(
            self,
            text="Focus Score: 0",
            font=("Helvetica", 16)
        )
        self.score_label.pack(pady=10)

        # ---------- SYSTEM MESSAGE ----------
        self.message_label = tk.Label(
            self,
            text="Stay focused.",
            font=("Helvetica", 12)
        )
        self.message_label.pack(pady=5)

        # ---------- TASK LIST ----------
        task_frame = tk.Frame(self)
        task_frame.pack(pady=10)

        tk.Label(task_frame, text="Tasks", font=("Helvetica", 14)).pack()

        self.tasks = []
        self.task_vars = []

        # Entry to add tasks
        self.task_entry = tk.Entry(task_frame, width=25)
        self.task_entry.pack(pady=5)

        tk.Button(
            task_frame,
            text="Add Task",
            command=self.add_task
        ).pack()

        # Task list display
        self.task_list_frame = tk.Frame(task_frame)
        self.task_list_frame.pack()

        # ---------- BACK BUTTON ----------
        tk.Button(
            self,
            text="Back",
            command=self.go_back
        ).pack(pady=10)

    # ---------- ADD TASK ----------
    def add_task(self):
        task = self.task_entry.get()
        if not task:
            return

        var = tk.IntVar()
        cb = tk.Checkbutton(
            self.task_list_frame,
            text=task,
            variable=var
        )
        cb.pack(anchor="w")

        self.tasks.append(task)
        self.task_vars.append(var)

        self.task_entry.delete(0, tk.END)

    # ---------- UPDATE SCORE ----------
    def update_score(self, score):
        self.score_label.config(text=f"Focus Score: {score}")

        # message logic
        if score < 40:
            self.message_label.config(text="You seem distracted...")
        elif score < 70:
            self.message_label.config(text="Try to focus more")
        else:
            self.message_label.config(text="Great focus! Keep it up.")

        self.update()
    
    # ---------- UPDATE CAMERA ----------

    def update_camera(self, frame):
        # Convert BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL image
        img = Image.fromarray(frame)
        img = img.resize((500, 350))              # Resize to fit label

        # Convert to Tkinter image
        imgtk = ImageTk.PhotoImage(image=img)

        # Show in label
        self.camera_label.config(image=imgtk, text="")
        self.camera_label.image = imgtk

    # ---------- BACK ----------
    def go_back(self):
        from ui.home import HomeScreen
        self.controller.show(HomeScreen)

