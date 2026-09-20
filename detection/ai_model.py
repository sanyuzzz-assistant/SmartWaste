import tensorflow as tf
import numpy as np


# ==============================
# SmartWaste AI Model
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


def predict_waste(image_path):
    """
    Predict waste category from an uploaded image.
    """

    # Load trained model
    model = tf.keras.models.load_model(MODEL_PATH)

    # Load image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    # Convert image to NumPy array
    image_array = tf.keras.utils.img_to_array(image)

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Normalize image
    image_array = image_array / 255.0

    # Make prediction
    predictions = model.predict(
        image_array,
        verbose=0
    )

    # Get predicted class
    predicted_index = np.argmax(
        predictions[0]
    )

    predicted_category = CLASS_NAMES[
        predicted_index
    ]

    # Get confidence
    confidence = float(
        predictions[0][predicted_index] * 100
    )

    return predicted_category, confidence