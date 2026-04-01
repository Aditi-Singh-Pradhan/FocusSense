"""
Adaptive Timer for FocusSense.
Combines:
- Time tracking (accurate)
- Focus streak tracking
- Fatigue detection (Flow logic)
"""

import time


class AdaptiveTimer:
    def __init__(self, avg_span=12):
        self.avg_span = avg_span
        self.current_streak = 0  # minutes
        self.focus_history = []

        self.last_popup_time = 0
        self.last_update_time = time.time()

    def update(self, focus_score):
        now = time.time()

        # REAL delta time tracking (not just increments)
        delta = (now - self.last_update_time) / 60
        self.last_update_time = now

        # track streak
        if focus_score > 60:
            self.current_streak += delta
        else:
            self.current_streak = 0

        # track history
        self.focus_history.append(focus_score)
        if len(self.focus_history) > 5:
            self.focus_history.pop(0)

    def is_declining(self):
        if len(self.focus_history) < 5:
            return False

        # smoother decline detection
        diffs = [
            self.focus_history[i] - self.focus_history[i + 1]
            for i in range(len(self.focus_history) - 1)
        ]

        # majority decreasing
        return sum(d > 0 for d in diffs) >= 3

    def should_suggest_break(self, focus_score):
        now = time.time()

        # cooldown
        if now - self.last_popup_time < 60:
            return False

        stretch_limit = self.avg_span * 1.3
        hard_limit = self.avg_span * 1.5

        # don't trigger too early
        if self.current_streak < self.avg_span * 0.7:
            return False

        # fatigue detection
        if (
            self.current_streak > self.avg_span and
            self.is_declining() and
            focus_score < 60   # slightly relaxed
        ):
            self.last_popup_time = now
            return True

        # hard cap
        if self.current_streak > hard_limit:
            self.last_popup_time = now
            return True

        return False

