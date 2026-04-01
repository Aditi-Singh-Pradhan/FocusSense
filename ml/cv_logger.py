"""
CV Logger for FocusSense.

Logs averaged focus data to CSV every fixed interval.
"""

import time
import csv
import os
from datetime import datetime


class CVLogger:
    def __init__(self, filename="data/focus_signals.csv"):
        self.filename = filename
        self.interval = 30  # seconds
        self.start_time = time.time()

        self.buffer = []

        # ensure directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        # create file if not exists
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "face",
                    "head",
                    "blink",
                    "focus_score",
                    "subject"
                ])

    def log(self, cv_data, focus_score, subject):
        # store full data
        self.buffer.append((cv_data, focus_score, subject))

        current_time = time.time()

        if current_time - self.start_time >= self.interval:
            self.flush()
            self.start_time = current_time

    def flush(self):
        if not self.buffer:
            return

        faces, heads, blinks, scores = [], [], [], []
        subjects = []

        for cv_data, score, subject in self.buffer:
            faces.append(cv_data.get("face", 0))
            heads.append(cv_data.get("head", 0))
            blinks.append(cv_data.get("blink", 0))
            scores.append(score)
            subjects.append(subject)

        # take most common subject in interval
        subject = max(set(subjects), key=subjects.count)

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(sum(faces) / len(faces), 2),
            round(sum(heads) / len(heads), 2),
            round(sum(blinks) / len(blinks), 4),
            round(sum(scores) / len(scores), 2),
            subject
        ]

        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        self.buffer = []

