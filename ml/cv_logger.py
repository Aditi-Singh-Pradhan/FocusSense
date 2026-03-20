import time
import csv
import os


class CVLogger:
    def __init__(self, filename="ml/dataset/focus_log.csv"):                                 # Initialize logger with filename and buffer
        self.filename = filename
        self.interval = 30

        self.buffer = []
        self.last_log_time = time.time()

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

    def log(self, cv_data, focus_score):                                                    # Add CV data and focus score to buffer, flush if interval has passed
        self.buffer.append((cv_data, focus_score))

        current_time = time.time()

        # Only log every interval
        if current_time - self.start_time >= self.interval:
            self.flush()
            self.start_time = current_time

    def flush(self):
        if not self.buffer:
            return

        faces = []
        heads = []
        blinks = []
        scores = []

        for cv_data, score in self.buffer:
            faces.append(cv_data.get("face", 0))
            heads.append(cv_data.get("head", 0))
            blinks.append(cv_data.get("blink", 0))
            scores.append(score)

        row = [
            time.time(),
            round(sum(scores) / len(scores), 2),
            round(sum(heads) / len(heads), 2),
            round(sum(blinks) / len(blinks), 4),
            round(sum(faces) / len(faces), 2)
        ]

        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        self.buffer = []