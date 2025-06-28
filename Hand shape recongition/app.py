import cv2
import mediapipe as mp
import math

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Fingertip landmark IDs
tip_ids = [4, 8, 12, 16, 20]

# Function to calculate Euclidean distance
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    total_fingers = 0

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lm_list = []
            h, w, _ = frame.shape
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if lm_list:
                label = handedness.classification[0].label  # 'Left' or 'Right'

                # --- Improved Thumb Detection using distance from palm ---
                thumb_tip = lm_list[4]
                index_mcp = lm_list[5]
                thumb_ip = lm_list[3]

                thumb_open = distance(thumb_tip, index_mcp) > 40  # Threshold may vary
                if thumb_open:
                    total_fingers += 1

                # Other 4 fingers
                for i in range(1, 5):
                    if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
                        total_fingers += 1

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show finger count
    cv2.rectangle(frame, (0, 0), (350, 100), (0, 0, 0), -1)
    cv2.putText(frame, f'Total Fingers: {total_fingers}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    cv2.imshow("Freehand Finger Number Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
