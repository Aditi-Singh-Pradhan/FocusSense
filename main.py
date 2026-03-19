def main():
    camera = Camera().start()
    cv_engine = CVEngine()
    activity_tracker = ActivityTracker()
    behavior_engine = BehaviorEngine()
    app = App()

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            cv_data = cv_engine.process_frame(frame)

            # unpack tuple
            category, score = activity_tracker.get_activity_score()
            activity_data = score

            focus_score = behavior_engine.compute_focus_score(cv_data, activity_data)

            # UPDATE UI
            app.update_score(focus_score)

            # OPTIONAL: keep camera window for now
            cv2.putText(frame, f"Focus Score: {focus_score}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("FocusSense", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.1)

    finally:
        camera.stop()
        cv2.destroyAllWindows()
