from ultralytics import YOLO
import cv2

# Trained YOLO model
model = YOLO(
    r"runs\detect\runs\detect\smartwaste_clean\weights\best.pt"
)

# Test image
image_path = r"yolo_clean_dataset\valid\images"

# Get first image from validation folder
import os

files = [
    f for f in os.listdir(image_path)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not files:
    print("No test images found.")
    exit()

test_image = os.path.join(image_path, files[0])

print("Testing image:")
print(test_image)

# Run detection
results = model(test_image, conf=0.25)

# Display result
annotated_image = results[0].plot()

cv2.imshow("SmartWaste - YOLO Test", annotated_image)

print("\nPress Q to close the image.")

while True:
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()