# FocusSense
### Attention & Productivity Assistant

FocusSense uses computer vision and behavioral ML to analyze your attention in real time, detect distraction and fatigue, and automatically adapt your study sessions — so you stop guessing and start studying smarter.

---

## What It Does

Most productivity tools treat every study session the same. FocusSense doesn't.

It watches how *you* actually focus — your patterns, your peak hours, your real attention span — and builds a study system around that, not around a generic 25-minute timer.

---

## Features

- **Real-time attention detection** — Uses your webcam to detect face presence, head direction, and blink rate
- **Focus Score** — A live 0–100 score updated every 30 seconds based on your behavior
- **App activity tracking** — Logs which apps you use during sessions and categorizes them
- **Smart break alerts** — Notifies you when fatigue or distraction crosses a threshold
- **Adaptive Pomodoro timer** — Adjusts session length based on your personal attention patterns
- **Session dashboard** — Visualizes focus score, session history, and attention trends
- **Subject tagging** — Tag sessions by subject to compare performance across topics
- **Distraction journal** — Auto-logs every distraction event with timestamp and active app
- **Best study time insights** — Learns when you focus best based on time-of-day patterns
- **Privacy-first** — All processing is 100% local. No data ever leaves your device.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Computer Vision | OpenCV, MediaPipe Face Mesh |
| Behavior Tracking | Python, psutil, pygetwindow |
| ML & Data | pandas, scikit-learn |
| Visualization | matplotlib, Tkinter |
| Notifications | plyer |
| Storage | Local CSV files |

---

## Project Structure

```
focussense/
├── main.py                 # Entry point
├── core/
│   ├── session.py          # Session management & Pomodoro logic
│   ├── behavior.py         # Focus score computation
│   ├── alerts.py           # Notification triggers
│   └── adaptive_timer.py   # ML-based timer adjustment
├── vision/
│   ├── camera.py           # Webcam capture (threaded)
│   └── cv_engine.py        # MediaPipe face/eye analysis
├── tracker/
│   └── activity.py         # Active app/window tracking
├── ml/
│   ├── data_logger.py      # Logs signals to CSV
│   └── predictor.py        # Attention pattern predictor
├── ui/
│   └── dashboard.py        # Live dashboard UI
└── data/                   # Auto-created on first run
    ├── sessions.csv
    ├── focus_signals.csv
    └── app_activity.csv
```

---

## Setup & Installation

### Prerequisites
- Python 3.8 – 3.11
- Webcam

### Install dependencies

```bash
pip install opencv-python mediapipe psutil pygetwindow plyer pandas matplotlib scikit-learn
```

### Run FocusSense

```bash
python main.py
```

The `data/` folder will be created automatically on first run.

---

## How It Works

```
Webcam Feed ──────────────────────────────────────────┐
                                                       |
                                             CV Engine (MediaPipe)
                                             - Face presence
                                             - Head direction
                                             - Blink rate
                                                       |
App Activity Tracker ──────────────────────────────────┤
- Active window title                                  |
- App category                               Behavior Tracker
                                             - Computes Focus Score (0-100)
                                             - Logs to CSV every 30s
                                                       |
                                       ┌───────────────┴───────────────┐
                                       |                               |
                                  Dashboard                       Alert System
                               Live focus score               Break reminders
                               Session history                Fatigue warnings
                               Attention trends               Distraction nudges
                                       |
                                  ML Predictor
                         Learns your patterns over time
                         Adapts session length automatically
```

---

## What Gets Tracked

| Signal | How | Why |
|---|---|---|
| Face presence | MediaPipe | Are you at your desk? |
| Head direction | MediaPipe landmarks | Are you looking at the screen? |
| Blink rate | Eye landmark distance | Fatigue detection |
| Active app | pygetwindow | Are you on task? |
| Session length | Timer | How long do you actually study? |
| Time of day | System clock | When do you focus best? |

---

## Roadmap

- [x] System architecture & design
- [x] CV Engine — face presence & blink detection
- [x] App activity tracker
- [ ] Focus score computation
- [ ] CSV data logging
- [ ] Live dashboard
- [ ] Alert system
- [ ] Adaptive timer (rule-based)
- [ ] ML predictor (pattern-based)
- [ ] Subject tagging
- [ ] Session goals & completion rating
- [ ] Best study time recommendations

---

## Privacy

FocusSense is built privacy-first by design:

- **No video is ever stored** — only derived numbers (blink rate, head direction score, etc.)
- **No internet connection required** — everything runs locally on your machine
- **Your data stays yours** — all logs are plain CSV files on your own device, readable and deletable at any time

---

## Author

Aditi Singh Pradhan
1st Year B.E. Computer Science — BITS Goa + RMIT (2+2 degree)
