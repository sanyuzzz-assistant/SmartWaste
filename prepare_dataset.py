import os
import shutil


# =========================================
# SmartWaste Dataset Preparation
# =========================================

# Extracted dataset location
SOURCE_DATASET = r"C:\Users\Lenovo\Downloads\Garbage_dataset_PlusYaml\Garbage_dataset_PlusYaml"

# SmartWaste project dataset location
PROJECT_DATASET = r"C:\Users\Lenovo\OneDrive\Documents\projects\SmartWaste\dataset"


# Dataset class ID -> SmartWaste folder
CLASS_NAMES = {
    0: "paper",
    1: "plastic",
    2: "glass",
    3: "metal",
    4: "organic",
    5: "e_waste",
    6: "general"
}


# Number of images required
TRAIN_PER_CLASS = 40
VALIDATION_PER_CLASS = 10


# Supported image extensions
IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png"
]


def prepare_split(split_name, images_needed):

    source_images = os.path.join(
        SOURCE_DATASET,
        split_name,
        "images"
    )

    source_labels = os.path.join(
        SOURCE_DATASET,
        split_name,
        "labels"
    )

    destination_root = os.path.join(
        PROJECT_DATASET,
        "train" if split_name == "train" else "validation"
    )


    print()
    print("=" * 50)
    print(f"Processing {split_name.upper()} dataset")
    print("=" * 50)


    for class_id, class_name in CLASS_NAMES.items():

        destination_folder = os.path.join(
            destination_root,
            class_name
        )

        os.makedirs(
            destination_folder,
            exist_ok=True
        )


        selected = 0


        for filename in os.listdir(source_images):

            if selected >= images_needed:
                break


            file_extension = os.path.splitext(
                filename
            )[1].lower()


            if file_extension not in IMAGE_EXTENSIONS:
                continue


            image_name = os.path.splitext(
                filename
            )[0]


            label_file = os.path.join(
                source_labels,
                image_name + ".txt"
            )


            if not os.path.exists(label_file):
                continue


            try:

                with open(
                    label_file,
                    "r"
                ) as file:

                    lines = [
                        line.strip()
                        for line in file
                        if line.strip()
                    ]


                if not lines:
                    continue


                # Get class IDs from label file
                class_ids = set()

                for line in lines:

                    parts = line.split()

                    if len(parts) >= 5:

                        detected_class_id = int(parts[0])

                        class_ids.add(
                            detected_class_id
                        )


                # Use only images containing
                # exactly one waste class
                if len(class_ids) != 1:
                    continue


                if class_id not in class_ids:
                    continue


                source_image = os.path.join(
                    source_images,
                    filename
                )


                destination_image = os.path.join(
                    destination_folder,
                    filename
                )


                shutil.copy2(
                    source_image,
                    destination_image
                )


                selected += 1


            except Exception as error:

                print(
                    f"Skipped {filename}: {error}"
                )


        print(
            f"{class_name}: {selected} images copied"
        )


        if selected < images_needed:

            print(
                f"WARNING: Only {selected} images found "
                f"for {class_name}"
            )


# =========================================
# Prepare Training Dataset
# =========================================

prepare_split(
    "train",
    TRAIN_PER_CLASS
)


# =========================================
# Prepare Validation Dataset
# =========================================

prepare_split(
    "valid",
    VALIDATION_PER_CLASS
)


print()
print("=" * 50)
print("DATASET PREPARATION COMPLETED")
print("=" * 50)
print()
print("Your SmartWaste dataset is ready.")
print("Training images: up to 280")
print("Validation images: up to 70")
print("Total: up to 350 images")