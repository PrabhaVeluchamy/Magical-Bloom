import cv2
import numpy as np
import math


# ---------------------------------
# Math Utilities
# ---------------------------------

def distance(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1]
    )


def midpoint(p1, p2):
    return (
        int((p1[0] + p2[0]) / 2),
        int((p1[1] + p2[1]) / 2)
    )


def lerp(current, target, speed=0.15):
    return current + (target - current) * speed


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


# ---------------------------------
# Image Utilities
# ---------------------------------

def resize_keep_ratio(image, target_size):

    if image is None:
        return None

    h, w = image.shape[:2]

    scale = target_size / max(h, w)

    nw = max(1, int(w * scale))
    nh = max(1, int(h * scale))

    interpolation = (
        cv2.INTER_AREA
        if scale < 1
        else cv2.INTER_CUBIC
    )

    return cv2.resize(
        image,
        (nw, nh),
        interpolation=interpolation
    )


def rotate_image(image, angle):

    h, w = image.shape[:2]

    center = (w / 2, h / 2)

    matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])

    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    matrix[0, 2] += (new_w / 2) - center[0]
    matrix[1, 2] += (new_h / 2) - center[1]

    return cv2.warpAffine(
        image,
        matrix,
        (new_w, new_h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0)
    )


# ---------------------------------
# PNG Overlay
# ---------------------------------

def overlay_png(background, overlay, x, y):

    if overlay is None:
        return

    bg_h, bg_w = background.shape[:2]
    h, w = overlay.shape[:2]

    if x >= bg_w or y >= bg_h:
        return

    if x + w <= 0 or y + h <= 0:
        return

    x1 = max(x, 0)
    y1 = max(y, 0)

    x2 = min(bg_w, x + w)
    y2 = min(bg_h, y + h)

    overlay = overlay[
        y1 - y:y2 - y,
        x1 - x:x2 - x
    ]

    roi = background[y1:y2, x1:x2]

    if overlay.shape[2] == 4:

        alpha = overlay[:, :, 3].astype(np.float32) / 255.0
        alpha = alpha[:, :, None]

        roi[:] = (
            overlay[:, :, :3] * alpha +
            roi * (1 - alpha)
        ).astype(np.uint8)

    else:

        roi[:] = overlay


# ---------------------------------
# Glow
# ---------------------------------

def draw_glow(frame, center, radius):

    overlay = frame.copy()

    for i in range(8):

        r = radius + i * 10

        alpha = max(0.02, 0.10 - i * 0.01)

        cv2.circle(
            overlay,
            center,
            r,
            (255, 180, 255),
            -1,
            cv2.LINE_AA
        )

        cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0,
            frame
        )


# ---------------------------------
# FPS
# ---------------------------------

class FPS:

    def __init__(self):

        self.prev = cv2.getTickCount()

    def update(self):

        current = cv2.getTickCount()

        fps = cv2.getTickFrequency() / (
            current - self.prev
        )

        self.prev = current

        return int(fps)