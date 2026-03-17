
import cv2
import threading


class Camera:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")

        self.frame = None
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        #Start camera thread
        if self.running:
            return self

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
        return self

    def update(self):
        #Continuously capture frames
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            with self.lock:
                self.frame = frame

    def get_frame(self):
        #Return latest frame safely
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        #Stop camera safely
        self.running = False
        if hasattr(self, "thread"):
            self.thread.join()
        self.cap.release()

