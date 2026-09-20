from ultralytics import YOLO
import cv2

# Load trained SmartWaste YOLO model
model = YOLO(
    r"runs\detect\runs\detect\smartwaste_clean\weights\best.pt"
)

# Open laptop webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("SmartWaste YOLO Live Detection Started")
print("Press Q to stop")

while True:

    success, frame = cap.read()

    if not success:
        print("Failed to read webcam frame.")
        break

    # YOLO detection
    results = model(
        frame,
        imgsz=320,
        conf=0.40,
        verbose=False
    )

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    # Show webcam window
    cv2.imshow(
        "SmartWaste - YOLO Live Detection",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Live detection stopped.")