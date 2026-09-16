import cv2
import mediapipe as mp
import math


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.results = None
        self.frame_width = 0
        self.frame_height = 0

    # --------------------------------------------

    def process(self, frame):

        self.frame_height, self.frame_width = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb)

    # --------------------------------------------

    def draw(self, frame):

        if self.results is None:
            return

        if self.results.multi_hand_landmarks:

            for hand in self.results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

    # --------------------------------------------

    def get_index_tip(self, hand_index):

        if self.results is None:
            return None

        if not self.results.multi_hand_landmarks:
            return None

        if hand_index >= len(self.results.multi_hand_landmarks):
            return None

        hand = self.results.multi_hand_landmarks[hand_index]

        tip = hand.landmark[8]

        return (
            int(tip.x * self.frame_width),
            int(tip.y * self.frame_height)
        )

    # --------------------------------------------

    def get_two_hand_center(self):

        p1 = self.get_index_tip(0)
        p2 = self.get_index_tip(1)

        if p1 is None or p2 is None:
            return None

        return (
            (p1[0] + p2[0]) // 2,
            (p1[1] + p2[1]) // 2
        )

    # --------------------------------------------

    def get_hand_distance(self):

        p1 = self.get_index_tip(0)
        p2 = self.get_index_tip(1)

        if p1 is None or p2 is None:
            return None

        return int(
            math.hypot(
                p2[0] - p1[0],
                p2[1] - p1[1]
            )
        )

    # --------------------------------------------

    def get_hand_angle(self):

        p1 = self.get_index_tip(0)
        p2 = self.get_index_tip(1)

        if p1 is None or p2 is None:
            return 0

        return math.degrees(
            math.atan2(
                p2[1] - p1[1],
                p2[0] - p1[0]
            )
        )

    # --------------------------------------------

    def close(self):

        self.hands.close()