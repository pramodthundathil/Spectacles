import cv2
import mediapipe as mp
import numpy as np

# Initialize Face Mesh Detector
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)



def glass_Analyse(glass_path):
# Load Glasses Image (Ensure the image has an alpha channel for transparency)
    glasses = cv2.imread(glass_path, cv2.IMREAD_UNCHANGED)

    # Start Video Capture
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get key facial points for glasses placement
                left_eye = np.array([face_landmarks.landmark[33].x * frame.shape[1], face_landmarks.landmark[33].y * frame.shape[0]])
                right_eye = np.array([face_landmarks.landmark[263].x * frame.shape[1], face_landmarks.landmark[263].y * frame.shape[0]])
                nose_bridge = np.array([face_landmarks.landmark[168].x * frame.shape[1], face_landmarks.landmark[168].y * frame.shape[0]])

                # Calculate width and height for glasses
                glasses_width = int(np.linalg.norm(left_eye - right_eye) * 2.0)  # Adjust scale
                glasses_height = int(glasses_width * glasses.shape[0] / glasses.shape[1])  # Maintain aspect ratio

                # Calculate position
                x_offset = int(nose_bridge[0] - glasses_width // 2)
                y_offset = int(nose_bridge[1] - glasses_height // 2)

                # Resize glasses
                resized_glasses = cv2.resize(glasses, (glasses_width, glasses_height))

                # Overlay the glasses
                for i in range(glasses_height):
                    for j in range(glasses_width):
                        if resized_glasses[i, j][3] > 0:  # Check transparency
                            y, x = y_offset + i, x_offset + j
                            if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                                frame[y, x] = resized_glasses[i, j][:3]

        # Show Output
        cv2.imshow("Virtual Glasses", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
