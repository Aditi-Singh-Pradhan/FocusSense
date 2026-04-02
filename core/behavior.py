"""
Behavior engine for computing focus score.

Combines computer vision signals and app activity data
to calculate a real-time focus score (0–100).
"""

from utils.config import (
    WEIGHT_FACE, WEIGHT_HEAD, WEIGHT_BLINK, WEIGHT_APP,
    SMOOTHING_FACTOR, BLINK_SCALE
)


class BehaviorEngine:
    def __init__(self):
        self.prev_score = None

    def compute_focus_score(self, cv_data, activity_data):

        # ---- SAFE EXTRACTION ----
        face = cv_data.get("face", 0)
        head = cv_data.get("head", 0)
        blink = cv_data.get("blink", 0)
        app = activity_data if activity_data is not None else 0

        # ---- NORMALIZE BLINK ----
        # smaller eye opening → fatigue → lower score
        blink_score = 1 - min(blink * BLINK_SCALE, 1)   # scaled + clamped

        # ---- RAW SCORE ----
        raw_score = (
            face * WEIGHT_FACE +
            head * WEIGHT_HEAD +
            blink_score * WEIGHT_BLINK +
            app * WEIGHT_APP
        )

        # ---- SMOOTHING ----
        if self.prev_score is None:
            smoothed = raw_score
        else:
            smoothed = SMOOTHING_FACTOR * self.prev_score + (1 - SMOOTHING_FACTOR) * raw_score

        self.prev_score = smoothed

        # ---- CLAMP ----
        smoothed = max(0, min(smoothed, 1))

        return round(smoothed * 100, 2)
