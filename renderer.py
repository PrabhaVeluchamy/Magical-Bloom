import cv2
import numpy as np


class Renderer:

    def __init__(self):

        self.previous_center = None

    # ---------------------------------

    def smooth(self, center):

        if self.previous_center is None:
            self.previous_center = center
            return center

        x = int(self.previous_center[0] * 0.80 + center[0] * 0.20)
        y = int(self.previous_center[1] * 0.80 + center[1] * 0.20)

        self.previous_center = (x, y)

        return self.previous_center

    # ---------------------------------

    def rotate(self, image, angle):

        h, w = image.shape[:2]

        M = cv2.getRotationMatrix2D(
            (w // 2, h // 2),
            angle,
            1.0
        )

        return cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0)
        )

    # ---------------------------------

    def resize(self, image, size):

        return cv2.resize(
            image,
            (size, size),
            interpolation=cv2.INTER_CUBIC
        )

    # ---------------------------------

    def overlay_png(self, frame, png, x, y):

        h, w = png.shape[:2]

        if x < 0 or y < 0:
            return

        if x + w > frame.shape[1]:
            return

        if y + h > frame.shape[0]:
            return

        if png.shape[2] == 4:

            alpha = png[:, :, 3] / 255.0

            for c in range(3):

                frame[y:y+h, x:x+w, c] = (
                    alpha * png[:, :, c] +
                    (1 - alpha) * frame[y:y+h, x:x+w, c]
                )

        else:

            frame[y:y+h, x:x+w] = png

    # ---------------------------------

    def glow(self, frame, center, radius):

        overlay = frame.copy()

        cv2.circle(
            overlay,
            center,
            radius,
            (255, 180, 255),
            -1,
            cv2.LINE_AA
        )

        cv2.addWeighted(
            overlay,
            0.18,
            frame,
            0.82,
            0,
            frame
        )

    # ---------------------------------

    def shadow(self, frame, center, size):

        overlay = frame.copy()

        cv2.ellipse(
            overlay,
            (center[0], center[1] + size // 3),
            (size // 3, size // 10),
            0,
            0,
            360,
            (0, 0, 0),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.25,
            frame,
            0.75,
            0,
            frame
        )

    # ---------------------------------

    def render(
        self,
        frame,
        flower,
        center,
        size,
        angle
    ):

        if flower is None:
            return

        center = self.smooth(center)

        self.glow(
            frame,
            center,
            int(size * 0.45)
        )

        self.shadow(
            frame,
            center,
            size
        )

        flower = self.resize(
            flower,
            size
        )

        flower = self.rotate(
            flower,
            angle
        )

        h, w = flower.shape[:2]

        x = center[0] - w // 2
        y = center[1] - h // 2

        self.overlay_png(
            frame,
            flower,
            x,
            y
        )