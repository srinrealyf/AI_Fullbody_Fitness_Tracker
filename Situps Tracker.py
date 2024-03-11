import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360.0 - angle
    return angle

stage = None
counter = 0
angle2 = 0

# Video Feed
# Define the codec and create VideoWriter object
out = cv2.VideoWriter('output.mp4', -1, 20.0, (640, 480))
cap = cv2.VideoCapture(1)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolour image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolour back to RGB
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for sit-ups (upper body)
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Calculate angles relevant to sit-ups
            angle = calculate_angle(shoulder, hip, knee)
            angle2 = calculate_angle(hip, knee, ankle)

            # Visualize
            cv2.putText(image, str(round(angle, 3)),
                        tuple(np.multiply(hip, [int(cap.get(3)), int(cap.get(4))]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(round(angle2, 3)),
                        tuple(np.multiply(ankle, [int(cap.get(3)), int(cap.get(4))]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            if angle > 150:
                stage = "down"
            if angle < 90 and stage == "down" and angle2 < 90:
                stage = "up"
                counter += 0.5  # Increment by 0.5 for each sit-up (assuming down and up make one complete sit-up)
        except:
            pass

        # Render counter rectangle rgb(250, 152, 58)
        cv2.rectangle(image, (0, 0), (225, 105), (500, 0, 0), -1)
        cv2.putText(image, "SIT-UPS", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(int(counter)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, "STRICT MODE ON", (15, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        if angle2 > 90:
            cv2.putText(image, "Keep Going! You Got This!", (15, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                        cv2.LINE_AA)
        else:
            cv2.putText(image, "Rest a Bit, and Go Again!", (15, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                        cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(221, 204, 130), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(57, 80, 229), thickness=2, circle_radius=2)
                                  )

        out.write(image)
        cv2.imshow("AI Sit-Ups Counter", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
