import cv2
import mediapipe as mp
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Mở video thay vì camera
cap = cv2.VideoCapture("hand.mp4")

if not cap.isOpened():
    print("Không mở được video")
    exit()

while True:
    success, frame = cap.read()
    if not success:
        print("Xong")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("MediaPipe Hands", frame)

    if cv2.waitKey(20) & 0xFF == 27:  # ESC để thoát
        break

cap.release()
cv2.destroyAllWindows()
