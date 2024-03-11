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

            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Calculate angles
            angle = calculate_angle(shoulder, elbow, wrist)
            angle2 = calculate_angle(hip, knee, ankle)

            # Visualize
            cv2.putText(image, str(round(angle, 3)),
                        tuple(np.multiply(elbow, [int(cap.get(3)), int(cap.get(4))]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(round(angle2, 3)),
                        tuple(np.multiply(hip, [int(cap.get(3)), int(cap.get(4))]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            if angle > 170:
                stage = "up"
            if angle < 65 and stage == "up" and angle2 > 150:
                stage = "down"
                counter += 0.5  # Increment by 0.5 for each push-up (assuming up and down make one complete push-up)
        except:
            pass

        # Render counter rectangle rgb(250, 152, 58)
        cv2.rectangle(image, (0, 0), (225, 105), (500, 0, 0), -1)
        cv2.putText(image, "PUSH-UPS", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(int(counter)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, "STRICT MODE ON", (15, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


        if angle2 < 65 and angle2 > 150:
            cv2.putText(image, "Maintain Panra Thambi", (15, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                        cv2.LINE_AA)
        else:
            cv2.putText(image, "Come On Gopal, You Can!", (15, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                        cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(221, 204, 130), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(57, 80, 229), thickness=2, circle_radius=2)
                                  )

        out.write(image)
        cv2.imshow("AI Push-Ups Counter", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
