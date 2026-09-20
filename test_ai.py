import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartwaste.settings")
django.setup()

from detection.ai_model import predict_waste

image_path = "dataset/validation/plastic"

for file_name in os.listdir(image_path):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        full_path = os.path.join(image_path, file_name)

        category, confidence = predict_waste(full_path)

        print("\n==============================")
        print("Image:", file_name)
        print("Predicted Category:", category)
        print("Confidence:", round(confidence, 2), "%")
        print("==============================")

        break