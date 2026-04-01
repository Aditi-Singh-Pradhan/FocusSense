"""
Stats screen for FocusSense.
Displays:
- Weekly focus hours
- Attention span
- Improvement %
- Time per subject
"""

import tkinter as tk
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

class StatsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        plt.ion()  # interactive mode for live updates

        tk.Label(self, text="Stats", font=("Helvetica", 20)).pack(pady=10)

        tk.Button(self, text="Weekly Focus Hours", command=self.weekly_stats).pack(pady=5)
        tk.Button(self, text="Estimate Attention Span", command=self.estimate_attention_span).pack(pady=5)
        tk.Button(self, text="Improvement %", command=self.improvement).pack(pady=5)
        tk.Button(self, text="Time by Subject", command=self.subject_stats).pack(pady=5)

        # Result display
        self.result_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

        tk.Button(self, text="Back", command=self.go_back).pack(pady=10)

    # -------- WEEKLY GRAPH --------
    def weekly_stats(self):
        daily_focus = defaultdict(float)

        try:
            with open("data/focus_signals.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date = row["timestamp"].split(" ")[0]
                    score = float(row["focus_score"])

                    if score > 60:
                        daily_focus[date] += 0.5  # 30 sec intervals = 0.5 hrs approx

        except FileNotFoundError:
            self.result_label.config(text="No data found")
            return

        # sort by date
        days = sorted(daily_focus.keys())
        values = [daily_focus[day] for day in days]

        plt.figure()
        plt.plot(days, values, marker='o')
        plt.title("Weekly Focus Hours")
        plt.xlabel("Date")
        plt.ylabel("Focus Time (mins approx)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # -------- ATTENTION SPAN --------
    def estimate_attention_span(self):
        spans = []
        current_span = 0

        try:
            with open("data/focus_signals.csv", "r") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    score = float(row["focus_score"])

                    if score > 60:
                        current_span += 1
                    else:
                        if current_span > 0:
                            spans.append(current_span)
                            current_span = 0

            if current_span > 0:
                spans.append(current_span)

            if not spans:
                self.result_label.config(text="Not enough data")
                return

            avg_span = sum(spans) / len(spans)

            # convert to minutes (assuming 30 sec interval)
            avg_minutes = avg_span * 0.5

            self.result_label.config(
                text=f"Attention Span: {round(avg_minutes, 2)} min"
            )

        except FileNotFoundError:
            self.result_label.config(text="No data found")

    # -------- IMPROVEMENT --------
    def improvement(self):
        data = []

        try:
            with open("data/focus_signals.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(float(row["focus_score"]))

        except FileNotFoundError:
            self.result_label.config(text="No data found")
            return

        if len(data) < 20:
            self.result_label.config(text="Not enough data")
            return

        mid = len(data) // 2
        first = data[:mid]
        second = data[mid:]

        avg1 = sum(first) / len(first)
        avg2 = sum(second) / len(second)

        change = ((avg2 - avg1) / avg1) * 100

        self.result_label.config(
            text=f"Improvement: {round(change, 2)}%"
        )

    # -------- SUBJECT GRAPH --------
    def subject_stats(self):
        subject_time = defaultdict(float)

        try:
            with open("data/focus_signals.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    subject = row.get("subject", "Unknown")
                    score = float(row["focus_score"])

                    if score > 60:
                        subject_time[subject] += 0.5

        except FileNotFoundError:
            self.result_label.config(text="No data found")
            return

        subjects = list(subject_time.keys())
        values = list(subject_time.values())

        plt.figure()
        plt.bar(subjects, values)
        plt.title("Time Spent per Subject")
        plt.ylabel("Focus Time (hrs approx)")
        plt.show()

    def go_back(self):
        from ui.home import HomeScreen
        self.controller.show(HomeScreen)

