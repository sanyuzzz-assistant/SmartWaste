import tensorflow as tf
import numpy as np
import os

# ==============================
# SmartWaste Image Prediction
# ==============================

MODEL_PATH = "model/waste_classifier.keras"

IMAGE_SIZE = (128, 128)

CLASS_NAMES = [
    "e_waste",
    "general",
    "glass",
    "metal",
    "organic",
    "paper",
    "plastic"
]

# Test image from validation dataset
IMAGE_PATH = "dataset/validation/plastic"

# Find first image
image_file = None

for filename in os.listdir(IMAGE_PATH):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_file = os.path.join(IMAGE_PATH, filename)
        break

if image_file is None:
    print("No image found in the selected folder.")
    exit()

print("Test Image:")
print(image_file)

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

print("\nModel loaded successfully.")

# Load image
image = tf.keras.utils.load_img(
    image_file,
    target_size=IMAGE_SIZE
)

# Convert image to array
image_array = tf.keras.utils.img_to_array(image)

# Add batch dimension
image_array = np.expand_dims(image_array, axis=0)

# Normalize
image_array = image_array / 255.0

# Prediction
predictions = model.predict(image_array, verbose=0)

predicted_index = np.argmax(predictions[0])

predicted_class = CLASS_NAMES[predicted_index]

confidence = predictions[0][predicted_index] * 100

print("\n===================================")
print("SMARTWASTE PREDICTION")
print("===================================")

print("Predicted Waste:", predicted_class)
print(f"Confidence: {confidence:.2f}%")

print("===================================")