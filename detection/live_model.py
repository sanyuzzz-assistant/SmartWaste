from ultralytics import YOLO

MODEL_PATH = r"runs\detect\runs\detect\smartwaste_clean\weights\best.pt"

model = YOLO(MODEL_PATH)

print("SmartWaste YOLO model loaded successfully.")