import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import Tracker

# Load the YOLO model
model = YOLO('yolov8s.pt')

# Function to capture RGB values on mouse movement
def capture_rgb(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colors_bgr = [x, y]
        print(colors_bgr)

# Set up the window and mouse callback
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', capture_rgb)

# Open the video file
cap = cv2.VideoCapture('veh2.mp4')

# Read class names from file
with open("coco.txt", "r") as file:
    class_list = file.read().split("\n")

frame_count = 0
tracker = Tracker()

# Define line positions
line_y1 = 322
line_y2 = 368
offset = 6

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1
    if frame_count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    detections = results[0].boxes.data
    df = pd.DataFrame(detections).astype("float")

    bbox_list = []

    for _, row in df.iterrows():
        x1, y1, x2, y2, _, class_id = map(int, row)
        class_name = class_list[class_id]
        if 'car' in class_name:
            bbox_list.append([x1, y1, x2, y2])

    tracked_bboxes = tracker.update(bbox_list)
    for bbox in tracked_bboxes:
        x3, y3, x4, y4, obj_id = bbox
        cx = (x3 + x4) // 2
        cy = (y3 + y4) // 2
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(frame, str(obj_id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

    # Uncomment the lines below to draw reference lines
    # cv2.line(frame, (274, line_y1), (814, line_y1), (255, 255, 255), 1)
    # cv2.line(frame, (177, line_y2), (927, line_y2), (255, 255, 255), 1)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
