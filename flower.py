import cv2
import numpy as np
import os


class Flower:

    def __init__(self, image_path):

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Flower image not found: {image_path}"
            )

        self.image = cv2.imread(
            image_path,
            cv2.IMREAD_UNCHANGED
        )

        if self.image is None:
            raise ValueError("Unable to load flower image.")

        # Crop transparent border
        self.image = self.crop_transparent(self.image)

        self.current_size = 150
        self.target_size = 150

    # -----------------------------------

    def crop_transparent(self, img):

        if img.shape[2] != 4:
            return img

        alpha = img[:, :, 3]

        coords = cv2.findNonZero(alpha)

        if coords is None:
            return img

        x, y, w, h = cv2.boundingRect(coords)

        return img[y:y+h, x:x+w]

    # -----------------------------------

    def update(self, target_size):

        self.target_size = target_size

        speed = 0.15

        self.current_size += (
            self.target_size -
            self.current_size
        ) * speed

    # -----------------------------------

    def get_size(self):

        return int(self.current_size)

    # -----------------------------------

    def reset(self):

        self.current_size = 150
        self.target_size = 150