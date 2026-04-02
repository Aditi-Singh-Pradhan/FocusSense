"""
Adaptive Timer for FocusSense.
Combines:
- Time tracking (accurate)
- Focus streak tracking
- Fatigue detection (Flow logic)
"""

import time
from utils.config import (
    DEFAULT_AVG_SPAN, FOCUS_THRESHOLD, BREAK_COOLDOWN,
    STREAK_EARLY_CUTOFF, STREAK_STRETCH, STREAK_HARD_LIMIT
)


class AdaptiveTimer:
    def __init__(self, avg_span=DEFAULT_AVG_SPAN):
        self.avg_span = avg_span
        self.current_streak = 0  # minutes
        self.focus_history = []

        self.last_popup_time = 0
        self.last_update_time = time.time()

        self.running = False
        self.start_time = None
        self.elapsed = 0.0  # seconds

    def start(self):
        if self.running:
            return
        self.running = True
        self.start_time = time.time()
        self.last_update_time = self.start_time

    def stop(self):
        if not self.running:
            return
        self.elapsed += time.time() - self.start_time
        self.start_time = None
        self.running = False

    def reset(self):
        self.running = False
        self.start_time = None
        self.elapsed = 0.0
        self.current_streak = 0
        self.focus_history = []
        self.last_update_time = time.time()

    def get_elapsed_seconds(self):
        if self.running and self.start_time is not None:
            return self.elapsed + (time.time() - self.start_time)
        return self.elapsed

    def update(self, focus_score):
        if not self.running:
            return

        now = time.time()

        # REAL delta time tracking (not just increments)
        delta = (now - self.last_update_time) / 60
        self.last_update_time = now

        # track streak
        if focus_score > FOCUS_THRESHOLD:
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
        if now - self.last_popup_time < BREAK_COOLDOWN:
            return False

        stretch_limit = self.avg_span * STREAK_STRETCH
        hard_limit = self.avg_span * STREAK_HARD_LIMIT

        # don't trigger too early
        if self.current_streak < self.avg_span * STREAK_EARLY_CUTOFF:
            return False

        # fatigue detection
        if (
            self.current_streak > self.avg_span and
            self.is_declining() and
            focus_score < FOCUS_THRESHOLD   # slightly relaxed
        ):
            self.last_popup_time = now
            return True

        # hard cap
        if self.current_streak > hard_limit:
            self.last_popup_time = now
            return True

        return False

