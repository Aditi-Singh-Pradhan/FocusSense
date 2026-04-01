"""
Adaptive Timer for FocusSense.
Combines:
- Time tracking
- Focus streak tracking
- Fatigue detection (Flow logic)
"""

import time


class AdaptiveTimer:
    def __init__(self, avg_span=12):
        self.start_time = time.time()

        # focus logic
        self.current_streak = 0  # in minutes
        self.avg_span = avg_span
        self.focus_history = []

        # popup control
        self.last_popup_time = 0

    def update(self, focus_score):
        # convert loop (~0.1s) to minutes
        delta = 0.1 / 60

        # track focus streak
        if focus_score > 60:
            self.current_streak += delta
        else:
            self.current_streak = 0

        # track history (last 5 values)
        self.focus_history.append(focus_score)
        if len(self.focus_history) > 5:
            self.focus_history.pop(0)

    def is_declining(self):
        if len(self.focus_history) < 5:
            return False

        return all(
            self.focus_history[i] > self.focus_history[i + 1]
            for i in range(len(self.focus_history) - 1)
        )

    def should_suggest_break(self, focus_score):
        now = time.time()

        # cooldown → avoid spam
        if now - self.last_popup_time < 60:
            return False

        stretch_limit = self.avg_span * 1.3
        hard_limit = self.avg_span * 1.5

        # fatigue detection
        if (
            self.current_streak > self.avg_span and
            self.is_declining() and
            focus_score < 55
        ):
            self.last_popup_time = now
            return True

        # hard cap (push boundary but not too far)
        if self.current_streak > hard_limit:
            self.last_popup_time = now
            return True

        return False

