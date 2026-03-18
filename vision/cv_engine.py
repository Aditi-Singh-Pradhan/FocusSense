import cv2
import mediapipe as mp


class CVEngine:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True
        )

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return {"face": 0, "head": 0, "blink": 0}

        landmarks = results.multi_face_landmarks[0].landmark

        return {
            "face": 1,
            "head": self.get_head_direction(landmarks),
            "blink": self.get_blink_metric(landmarks),
        }

    def get_head_direction(self, landmarks):
        nose = landmarks[1]
        left = landmarks[234]
        right = landmarks[454]

        center = (left.x + right.x) / 2
        deviation = abs(nose.x - center)

        return max(0, 1 - deviation * 5)

    def get_blink_metric(self, landmarks):
        top_l = landmarks[159]
        bottom_l = landmarks[145]

        top_r = landmarks[386]
        bottom_r = landmarks[374]

        left_eye = abs(top_l.y - bottom_l.y)
        right_eye = abs(top_r.y - bottom_r.y)

        return (left_eye + right_eye) / 2
