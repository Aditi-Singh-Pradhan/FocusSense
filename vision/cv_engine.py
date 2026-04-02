"""
Computer Vision engine using MediaPipe.

Extracts attention-related signals:
- face presence
- head direction
- normalized blink metric
"""

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
            return None

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
        # ---- LEFT EYE ----
        top_l = landmarks[159]
        bottom_l = landmarks[145]
        left_l = landmarks[33]
        right_l = landmarks[133]

        vertical_l = abs(top_l.y - bottom_l.y)
        horizontal_l = abs(left_l.x - right_l.x)

        # ---- RIGHT EYE ----
        top_r = landmarks[386]
        bottom_r = landmarks[374]
        left_r = landmarks[362]
        right_r = landmarks[263]

        vertical_r = abs(top_r.y - bottom_r.y)
        horizontal_r = abs(left_r.x - right_r.x)

        # avoid division by zero
        if horizontal_l == 0 or horizontal_r == 0:
            return 0

        # normalized eye openness
        left_eye_ratio = vertical_l / horizontal_l
        right_eye_ratio = vertical_r / horizontal_r

        return (left_eye_ratio + right_eye_ratio) / 2

