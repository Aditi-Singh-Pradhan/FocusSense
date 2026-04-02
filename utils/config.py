"""
FocusSense Configuration
Central place for all constants and thresholds.
"""

# ---- CAMERA ----
CAMERA_SRC = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS_CAP = 30

# ---- FOCUS SCORE WEIGHTS ----
WEIGHT_FACE = 0.4
WEIGHT_HEAD = 0.3
WEIGHT_BLINK = 0.2
WEIGHT_APP = 0.1

# ---- SMOOTHING ----
SMOOTHING_FACTOR = 0.7  # higher = smoother but slower to react

# ---- BLINK ----
BLINK_SCALE = 8  # scaling factor for eye aspect ratio normalization

# ---- THRESHOLDS ----
FOCUS_THRESHOLD = 60       # below this = distracted
LOW_FOCUS_THRESHOLD = 40   # below this = very distracted

# ---- LOGGING ----
LOG_INTERVAL = 30          # seconds between CSV writes
LOG_FILE = "data/focus_signals.csv"

# ---- ADAPTIVE TIMER ----
DEFAULT_AVG_SPAN = 12      # minutes
BREAK_COOLDOWN = 60        # seconds between break popups
STREAK_EARLY_CUTOFF = 0.7  # don't suggest break before 70% of avg span
STREAK_STRETCH = 1.3
STREAK_HARD_LIMIT = 1.5

# ---- ACTIVITY TRACKING ----
PRODUCTIVE_APPS = ["Visual Studio Code", "Brave Browser"]
DISTRACTING_APPS = ["Spotify", "YouTube"]

# ---- UI ----
WINDOW_SIZE = "900x600"
SIDEBAR_BG = "#222"
SIDEBAR_ACTIVE_BG = "#444"
TIMER_REFRESH_MS = 500     # how often timer label updates (ms)