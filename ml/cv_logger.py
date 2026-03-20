import time
import csv
import os


class CVLogger:
    def __init__(self, filename="ml/dataset/focus_log.csv"):
        self.filename = filename

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        # Create file with headers if not exists
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "face",
                    "head",
                    "blink",
                    "focus_score"
                ])

    def log(self, cv_data, focus_score):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                time.time(),
                cv_data.get("face"),
                cv_data.get("head"),
                cv_data.get("blink"),
                focus_score
            ])