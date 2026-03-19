"""
Main application entry point. 
Runs the full FocusSense pipeline: 
Camera → CV Engine → Activity Tracker → Behavior Engine 
"""

from vision.camera import Camera
from core.behavior import BehaviorEngine    
from tracker.activity import ActivityTracker
from vision.cv_engine import CVEngine

import time
import cv2


def main():
    # Initialize components
    camera = Camera().start()
    cv_engine = CVEngine()
    activity_tracker = ActivityTracker()
    behavior_engine = BehaviorEngine()

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            cv_data = cv_engine.process_frame(frame)
            activity_data = activity_tracker.get_activity_score()

            focus_score = behavior_engine.compute_focus_score(cv_data, activity_data)

            # show score on screen
            cv2.putText(frame, f"Focus Score: {focus_score}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("FocusSense", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.1)

    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

