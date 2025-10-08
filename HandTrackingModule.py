import cv2
import mediapipe as mp

def get_hands():
    my_hands = mp.solutions.hands
    my_drawing = mp.solutions.drawing_utils
    hands = my_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    return hands, my_hands, my_drawing

def draw_hands(image, hands, my_hands, my_drawing):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Phát hiện bàn tay
    results = hands.process(rgb_image)

    all_hands = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Vẽ bàn tay
            my_drawing.draw_landmarks(
                image,
                hand_landmarks,
                my_hands.HAND_CONNECTIONS,
                # connections=None,
                landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2,
                                                                             circle_radius=3),
                connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1)
            )

            # Lấy toạ độ pixel của 21 điểm
            h, w, c = image.shape
            landmarks = []
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))
            all_hands.append(landmarks)

    return image, all_hands

def get_hand_positions(image, hands):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    h, w, c = image.shape
    positions = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for _, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                positions.append((cx, cy))
    return positions


