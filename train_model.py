# pyright: reportMissingModuleSource=false
import tensorflow as tf
from tensorflow.keras import layers, models
import os

# ==============================
# SmartWaste CNN Model Training
# ==============================

TRAIN_DIR = "dataset/train"
VALIDATION_DIR = "dataset/validation"

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 16
EPOCHS = 10

# Load training dataset
train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

# Load validation dataset
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Get class names
class_names = train_dataset.class_names

print("\nWaste Categories:")
for index, class_name in enumerate(class_names):
    print(index, "->", class_name)

# Normalize image pixels
normalization_layer = layers.Rescaling(1.0 / 255)

train_dataset = train_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

validation_dataset = validation_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

# ==============================
# CNN Model
# ==============================

model = models.Sequential([

    layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        input_shape=(128, 128, 3)
    ),

    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),

    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(0.5),

    layers.Dense(
        len(class_names),
        activation="softmax"
    )
])

# ==============================
# Compile Model
# ==============================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Display model structure
model.summary()

# ==============================
# Train Model
# ==============================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)

# ==============================
# Save Model
# ==============================

os.makedirs("model", exist_ok=True)

model.save("model/waste_classifier.keras")

print("\n===================================")
print("MODEL TRAINING COMPLETED")
print("===================================")
print("Model saved at:")
print("model/waste_classifier.keras")