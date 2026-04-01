import threading
import time
import cv2

from ui import app
from ui.focusmode import FocusModeScreen
from vision.camera import Camera
from vision.cv_engine import CVEngine
from tracker.activity import ActivityTracker
from core.behavior import BehaviorEngine
from ui.app import App
from ml.cv_logger import CVLogger
from core.adaptive_timer import AdaptiveTimer


def run_cv_loop(app):
    camera = Camera().start()
    cv_engine = CVEngine()
    timer = AdaptiveTimer(avg_span=12)  
    logger = CVLogger()
    activity_tracker = ActivityTracker()
    behavior_engine = BehaviorEngine()

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            cv_data = cv_engine.process_frame(frame)

            category, score = activity_tracker.get_activity_score()
            activity_data = score

            focus_score = behavior_engine.compute_focus_score(cv_data, activity_data)
            subject = app.current_subject

            logger.log(cv_data, focus_score, subject)

            app.update_camera(frame)
            app.update_score(focus_score)

            timer.update(focus_score)

            if timer.should_suggest_break(focus_score):
                app.root.after(0, lambda: app.frames[FocusModeScreen].show_break_popup(timer.current_streak))

    finally:
        camera.stop()
        cv2.destroyAllWindows()

