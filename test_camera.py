import cv2
from vision.camera import Camera

cam = Camera().start()

while True:
    frame = cam.get_frame()

    if frame is not None:
        cv2.imshow("FocusSense Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.stop()
cv2.destroyAllWindows()
