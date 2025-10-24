# test_yolo.py
from ultralytics import YOLO

# Load model YOLOv8n (nano)
model = YOLO('yolov8n.pt')


print("YOLOv8n berhasil di-install!")
# print(f"Model path: {model}")