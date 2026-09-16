import cv2

from hand_tracker import HandTracker
from flower import Flower
from renderer import Renderer
from animation import Animation
from particles import ParticleSystem

WINDOW_NAME = "MagicBloom AR"


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    tracker = HandTracker()
    flower = Flower("assets/flower.png")
    renderer = Renderer()
    animation = Animation()
    particles = ParticleSystem()

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    prev_tick = cv2.getTickCount()

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        # ----------------------------
        # Detect Hands
        # ----------------------------

        tracker.process(frame)
        tracker.draw(frame)

        center = tracker.get_two_hand_center()
        distance = tracker.get_hand_distance()
        angle = tracker.get_hand_angle()

        # ----------------------------
        # Animation
        # ----------------------------

        animation.update(distance)
        flower.update(animation.get_size())

        # ----------------------------
        # Draw Flower
        # ----------------------------

        if center is not None:

            center = (
                center[0],
                center[1] + animation.get_float()
            )

            particles.emit(center, 3)

            renderer.render(
                frame,
                flower.image,
                center,
                flower.get_size(),
                angle
            )

        # ----------------------------
        # Draw Particles
        # ----------------------------

        particles.update()
        particles.draw(frame)

        # ----------------------------
        # FPS
        # ----------------------------

        current_tick = cv2.getTickCount()

        fps = cv2.getTickFrequency() / (current_tick - prev_tick)

        prev_tick = current_tick

        cv2.putText(
            frame,
            f"FPS : {int(fps)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        if distance is not None:

            cv2.putText(
                frame,
                f"Distance : {distance}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        cv2.putText(
            frame,
            f"Flower Size : {flower.get_size()}",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        hand_count = 0

        if tracker.results is not None:
            if tracker.results.multi_hand_landmarks:
                hand_count = len(tracker.results.multi_hand_landmarks)

        cv2.putText(
            frame,
            f"Hands : {hand_count}",
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Move hands apart to enlarge flower",
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 255),
            2
        )

        cv2.putText(
            frame,
            "Q / ESC : Exit",
            (20, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    tracker.close()

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()