import threading
import time
import cv2

from vision.camera import Camera
from vision.cv_engine import CVEngine
from tracker.activity import ActivityTracker
from core.behavior import BehaviorEngine
from ui.app import App
from ml.cv_logger import CVLogger


def run_cv_loop(app):
    camera = Camera().start()                       # Start camera feed
    cv_engine = CVEngine()                          # Initialize CV engine
    logger = CVLogger()                             # Initialize CV logger
    activity_tracker = ActivityTracker()            # Initialize activity tracker
    behavior_engine = BehaviorEngine()              # Initialize behavior engine

    try:
        while True:
            frame = camera.get_frame()                          # Get latest camera frame
            if frame is None:
                continue

            cv_data = cv_engine.process_frame(frame)             # Extract CV features (face, head, blink)

            # Get activity score
            category, score = activity_tracker.get_activity_score()
            activity_data = score
            focus_score = behavior_engine.compute_focus_score(cv_data, activity_data)

            #csv logging
            logger.log(cv_data, focus_score)

            # Update UI
            app.update_camera(frame)
            app.update_score(focus_score)


            # (optional debug window)
            cv2.putText(frame, f"Focus Score: {focus_score}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()


def main():
    app = App()

    # Run CV in separate thread
    threading.Thread(target=run_cv_loop, args=(app,), daemon=True).start()

    #Run UI properly
    app.run()


if __name__ == "__main__":
    main()
