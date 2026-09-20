from pathlib import Path
import shutil
import random

# Original YOLO dataset
SOURCE = Path(
    r"C:\Users\Lenovo\Downloads\Garbage_dataset_PlusYaml\Garbage_dataset_PlusYaml"
)

# New small dataset
DEST = Path("yolo_small_dataset")

TRAIN_IMAGES = SOURCE / "train" / "images"
TRAIN_LABELS = SOURCE / "train" / "labels"

DEST_IMAGES = DEST / "train" / "images"
DEST_LABELS = DEST / "train" / "labels"

DEST_IMAGES.mkdir(parents=True, exist_ok=True)
DEST_LABELS.mkdir(parents=True, exist_ok=True)

# YOLO class IDs
CLASS_NAMES = {
    0: "Paper",
    1: "Plastic",
    2: "Glass",
    3: "Metal",
    4: "Organic",
    5: "Electronics",
    6: "Miscellaneous",
}

IMAGES_PER_CLASS = 100

random.seed(42)

# Store image files for each class
class_images = {class_id: [] for class_id in CLASS_NAMES}

# Read every YOLO label file
for label_file in TRAIN_LABELS.glob("*.txt"):

    lines = label_file.read_text(encoding="utf-8").splitlines()

    class_ids_in_image = set()

    for line in lines:
        parts = line.split()

        if parts:
            class_id = int(parts[0])

            if class_id in CLASS_NAMES:
                class_ids_in_image.add(class_id)

    image_file = None

    for extension in [".jpg", ".jpeg", ".png"]:
        possible_image = TRAIN_IMAGES / (label_file.stem + extension)

        if possible_image.exists():
            image_file = possible_image
            break

    if image_file is None:
        continue

    # Add image to every class it contains
    for class_id in class_ids_in_image:
        class_images[class_id].append(
            (image_file, label_file)
        )


print("\nAvailable images by class:")
for class_id, name in CLASS_NAMES.items():
    print(
        f"{class_id} - {name}: "
        f"{len(class_images[class_id])}"
    )


# Select images
selected_images = set()

for class_id, name in CLASS_NAMES.items():

    available = class_images[class_id]

    random.shuffle(available)

    selected = available[:IMAGES_PER_CLASS]

    for image_file, label_file in selected:
        selected_images.add(
            (image_file, label_file)
        )

    print(
        f"Selected for {name}: "
        f"{len(selected)}"
    )


# Copy selected images and labels
for image_file, label_file in selected_images:

    shutil.copy2(
        image_file,
        DEST_IMAGES / image_file.name
    )

    shutil.copy2(
        label_file,
        DEST_LABELS / label_file.name
    )


# Create data.yaml
data_yaml = f"""path: {DEST.resolve()}
train: train/images
val: train/images

names:
  0: Paper
  1: Plastic
  2: Glass
  3: Metal
  4: Organic
  5: Electronics
  6: Miscellaneous
"""

(DEST / "data.yaml").write_text(
    data_yaml,
    encoding="utf-8"
)

print("\n======================================")
print("SMALL YOLO DATASET CREATED")
print("======================================")

print(f"Dataset location: {DEST.resolve()}")
print(f"Total selected images: {len(selected_images)}")
print("data.yaml created successfully.")