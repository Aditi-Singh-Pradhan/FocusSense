
import cv2
from vision.camera import Camera
from vision.cv_engine import CVEngine


cam = Camera().start()
cv_engine = CVEngine()

while True:
    frame = cam.get_frame()

    if frame is not None:
        data = cv_engine.process_frame(frame)

        cv2.putText(frame, f"Face: {data['face']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, f"Head: {data['head']:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.putText(frame, f"Blink: {data['blink']:.4f}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.imshow("FocusSense CV Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.stop()
cv2.destroyAllWindows()

