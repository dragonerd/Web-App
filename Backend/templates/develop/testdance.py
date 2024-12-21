import cv2
import mediapipe as mp

# Initialize MediaPipe Pose (access through solutions submodule)
# Create VideoCapture object
cap = cv2.VideoCapture(0) 
cap = cv2.VideoCapture("http://192.168.1.4:4747/video")  # Replace 0 with your video file path if using a video file

# Define video recording flag (set to True for recording)
recording = False

# Define video codec and create VideoWriter object (if recording)
if recording:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB format for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Perform pose detection
    mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    results = mp_pose.process(rgb_frame)

    # Draw skeleton lines and joints on the frame (if results are available)
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks)

    # Display the frame with the skeleton
    cv2.imshow('frame with skeleton', frame)

    # Write frame to video (if recording)
    if recording:
        out.write(frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
if recording:
    out.release()
cv2.destroyAllWindows()
