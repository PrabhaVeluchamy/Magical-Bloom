import random
import cv2


class Particle:

    def __init__(self, center):

        self.x = center[0]
        self.y = center[1]

        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-4, -1)

        self.life = random.randint(25, 45)

        self.radius = random.randint(2, 5)

        self.color = (
            random.randint(180, 255),
            random.randint(100, 255),
            random.randint(180, 255)
        )

    # --------------------------

    def update(self):

        self.x += self.dx
        self.y += self.dy

        self.dy += 0.05

        self.life -= 1

    # --------------------------

    def draw(self, frame):

        if self.life <= 0:
            return

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius,
            self.color,
            -1,
            cv2.LINE_AA
        )

    # --------------------------

    def dead(self):

        return self.life <= 0


# ===================================


class ParticleSystem:

    def __init__(self):

        self.particles = []

    # --------------------------

    def emit(self, center, count=2):

        for _ in range(count):
            self.particles.append(
                Particle(center)
            )

    # --------------------------

    def update(self):

        alive = []

        for particle in self.particles:

            particle.update()

            if not particle.dead():
                alive.append(particle)

        self.particles = alive

    # --------------------------

    def draw(self, frame):

        for particle in self.particles:

            particle.draw(frame)

    # --------------------------

    def clear(self):

        self.particles.clear()