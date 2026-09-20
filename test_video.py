from ultralytics import YOLO
import cv2

model = YOLO(
    r"runs\detect\runs\detect\smartwaste_clean\weights\best.pt"
)

video_path = r"C:\Users\Lenovo\Downloads\WhatsApp Video 2026-09-20 at 12.04.04 AM.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    success, frame = cap.read()

    if not success:
        break

    results = model(
        frame,
        imgsz=320,
        conf=0.25,
        verbose=False
    )

    annotated_frame = results[0].plot()

    cv2.imshow(
        "SmartWaste - Video Detection",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()