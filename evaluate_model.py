import tensorflow as tf

# ==============================
# SmartWaste Model Evaluation
# ==============================

MODEL_PATH = "model/waste_classifier.keras"
VALIDATION_DIR = "dataset/validation"

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 16

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

print("Trained model loaded successfully.")

# Load validation dataset
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Get class names BEFORE normalization
class_names = validation_dataset.class_names

# Normalize images
normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)

validation_dataset = validation_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

print("\nWaste Categories:")
for index, class_name in enumerate(class_names):
    print(index, "->", class_name)

# Evaluate model
loss, accuracy = model.evaluate(validation_dataset, verbose=1)

print("\n===================================")
print("MODEL EVALUATION COMPLETED")
print("===================================")
print(f"Validation Loss: {loss:.4f}")
print(f"Validation Accuracy: {accuracy * 100:.2f}%")