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


def run_cv_loop(app, timer):
    camera = Camera().start()
    cv_engine = CVEngine()
    logger = CVLogger()
    activity_tracker = ActivityTracker()
    behavior_engine = BehaviorEngine()

    try:
        while True:
            frame = camera.get_frame()
            
            #flip frame for mirror effect (optional)
            frame = cv2.flip(frame, 1)

            if frame is None:
                continue

            cv_data = cv_engine.process_frame(frame)

            category, score = activity_tracker.get_activity_score()
            activity_data = score

            focus_score = behavior_engine.compute_focus_score(cv_data, activity_data)
            subject = app.current_subject

            logger.log(cv_data, focus_score, subject)

            # UI updates must be done in the main thread
            app.update_camera(frame)
            app.update_score(focus_score)

            # adaptive timer logic (only while running)
            if timer.running:
                timer.update(focus_score)

                if timer.should_suggest_break(focus_score):
                    app.root.after(0, lambda: app.frames[FocusModeScreen].show_break_popup(timer.current_streak))

    finally:
        camera.stop()
        cv2.destroyAllWindows()


def main():
    print("Starting Focussense App...")

    app = App()
    timer = AdaptiveTimer(avg_span=12)

    # wire timer into FocusMode screen
    app.frames[FocusModeScreen].set_timer(timer)

    threading.Thread(target=run_cv_loop, args=(app, timer), daemon=True).start()

    # Start the UI main loop
    app.run()

if __name__ == "__main__":
    main()
