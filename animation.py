import math


class Animation:

    def __init__(self):

        self.current_size = 150
        self.target_size = 150

        self.float_offset = 0
        self.rotation = 0
        self.glow_scale = 1.0

        self.frame = 0

    # ----------------------------------------

    def update(self, hand_distance):

        self.frame += 1

        # Default size when only one hand/no hands
        if hand_distance is None:

            self.target_size = 150

        else:

            # Scale flower based on hand distance
            # Distance 50  -> Size 100
            # Distance 200 -> Size 300
            # Distance 400 -> Size 600

            self.target_size = max(
                100,
                min(
                    650,
                    int(hand_distance * 1.5)
                )
            )

        # Smooth animation

        speed = 0.15

        self.current_size += (
            self.target_size -
            self.current_size
        ) * speed

        # Floating animation

        self.float_offset = math.sin(
            self.frame * 0.05
        ) * 8

        # Rotation animation

        self.rotation += 0.5

        if self.rotation >= 360:
            self.rotation = 0

        # Glow pulse

        self.glow_scale = (
            1 +
            0.15 *
            math.sin(self.frame * 0.08)
        )

    # ----------------------------------------

    def get_size(self):
        return int(self.current_size)

    # ----------------------------------------

    def get_float(self):
        return int(self.float_offset)

    # ----------------------------------------

    def get_rotation(self):
        return self.rotation

    # ----------------------------------------

    def get_glow_scale(self):
        return self.glow_scale

    # ----------------------------------------

    def reset(self):

        self.current_size = 150
        self.target_size = 150
        self.frame = 0
        self.rotation = 0
        self.float_offset = 0
        self.glow_scale = 1.0