from pathlib import Path
import shutil
import random

SOURCE = Path(
    r"C:\Users\Lenovo\Downloads\Garbage_dataset_PlusYaml\Garbage_dataset_PlusYaml"
)

DEST = Path("yolo_clean_dataset")

SOURCE_IMAGES = SOURCE / "train" / "images"
SOURCE_LABELS = SOURCE / "train" / "labels"

DEST_TRAIN_IMAGES = DEST / "train" / "images"
DEST_TRAIN_LABELS = DEST / "train" / "labels"

DEST_VAL_IMAGES = DEST / "valid" / "images"
DEST_VAL_LABELS = DEST / "valid" / "labels"

for folder in [
    DEST_TRAIN_IMAGES,
    DEST_TRAIN_LABELS,
    DEST_VAL_IMAGES,
    DEST_VAL_LABELS
]:
    folder.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = {
    0: "Paper",
    1: "Plastic",
    2: "Glass",
    3: "Metal",
    4: "Organic",
    5: "Electronics",
    6: "Miscellaneous"
}

# Very small dataset to protect laptop performance
TRAIN_PER_CLASS = 60
VAL_PER_CLASS = 20

random.seed(42)

class_images = {class_id: [] for class_id in CLASS_NAMES}

# Find images containing ONLY ONE class
for label_file in SOURCE_LABELS.glob("*.txt"):

    lines = label_file.read_text(
        encoding="utf-8"
    ).splitlines()

    class_ids = set()

    for line in lines:
        parts = line.split()

        if parts:
            class_ids.add(int(parts[0]))

    # Keep only single-class images
    if len(class_ids) != 1:
        continue

    class_id = list(class_ids)[0]

    if class_id not in CLASS_NAMES:
        continue

    image_file = None

    for extension in [".jpg", ".jpeg", ".png"]:
        candidate = SOURCE_IMAGES / (
            label_file.stem + extension
        )

        if candidate.exists():
            image_file = candidate
            break

    if image_file:
        class_images[class_id].append(
            (image_file, label_file)
        )


print("\nSingle-class images available:")

for class_id, name in CLASS_NAMES.items():
    print(
        f"{class_id} - {name}: "
        f"{len(class_images[class_id])}"
    )


# Select balanced images
for class_id, name in CLASS_NAMES.items():

    random.shuffle(class_images[class_id])

    selected = class_images[class_id][
        :TRAIN_PER_CLASS + VAL_PER_CLASS
    ]

    train_files = selected[:TRAIN_PER_CLASS]
    val_files = selected[TRAIN_PER_CLASS:]

    print(
        f"{name}: "
        f"{len(train_files)} train, "
        f"{len(val_files)} validation"
    )

    for image_file, label_file in train_files:

        shutil.copy2(
            image_file,
            DEST_TRAIN_IMAGES / image_file.name
        )

        shutil.copy2(
            label_file,
            DEST_TRAIN_LABELS / label_file.name
        )

    for image_file, label_file in val_files:

        shutil.copy2(
            image_file,
            DEST_VAL_IMAGES / image_file.name
        )

        shutil.copy2(
            label_file,
            DEST_VAL_LABELS / label_file.name
        )


# Create data.yaml
data_yaml = f"""path: {DEST.resolve()}
train: train/images
val: valid/images

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
print("CLEAN YOLO DATASET CREATED")
print("======================================")
print(f"Location: {DEST.resolve()}")