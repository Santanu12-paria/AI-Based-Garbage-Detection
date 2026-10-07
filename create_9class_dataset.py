import os
import shutil
import yaml

# ==========================================
# 1. Paths
# ==========================================

SOURCE = "dataset"
OUTPUT = "dataset_9class"

# ==========================================
# 2. Classes we want to keep
# ==========================================

selected_classes = {
    1: 0,    # Aluminum can
    3: 1,    # Cardboard
    12: 2,   # Glass bottle
    17: 3,   # Organic
    18: 4,   # Paper
    23: 5,   # Plastic bag
    24: 6,   # Plastic bottle
    28: 7,   # Plastic cup
    38: 8    # Tin
}

class_names = [
    "Aluminum can",
    "Cardboard",
    "Glass bottle",
    "Organic",
    "Paper",
    "Plastic bag",
    "Plastic bottle",
    "Plastic cup",
    "Tin"
]

# ==========================================
# 3. Create output folders
# ==========================================

for split in ["train", "valid", "test"]:

    os.makedirs(
        os.path.join(OUTPUT, split, "images"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT, split, "labels"),
        exist_ok=True
    )

# ==========================================
# 4. Process train, valid and test
# ==========================================

for split in ["train", "valid", "test"]:

    image_folder = os.path.join(SOURCE, split, "images")
    label_folder = os.path.join(SOURCE, split, "labels")

    output_image_folder = os.path.join(
        OUTPUT, split, "images"
    )

    output_label_folder = os.path.join(
        OUTPUT, split, "labels"
    )

    if not os.path.exists(label_folder):
        print(f"Skipping {split}: labels folder not found")
        continue

    processed = 0

    for label_file in os.listdir(label_folder):

        if not label_file.endswith(".txt"):
            continue

        label_path = os.path.join(label_folder, label_file)

        new_labels = []

        with open(label_path, "r") as f:

            for line in f:

                parts = line.strip().split()

                if len(parts) != 5:
                    continue

                old_class = int(parts[0])

                # Keep only selected classes
                if old_class in selected_classes:

                    new_class = selected_classes[old_class]

                    parts[0] = str(new_class)

                    new_labels.append(" ".join(parts))

        # Only keep images containing our selected classes
        if len(new_labels) > 0:

            # Copy image
            image_name = os.path.splitext(label_file)[0]

            possible_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".JPG",
                ".JPEG",
                ".PNG"
            ]

            image_path = None

            for ext in possible_extensions:

                candidate = os.path.join(
                    image_folder,
                    image_name + ext
                )

                if os.path.exists(candidate):
                    image_path = candidate
                    break

            if image_path is None:
                continue

            shutil.copy2(
                image_path,
                os.path.join(
                    output_image_folder,
                    os.path.basename(image_path)
                )
            )

            # Save new label
            new_label_path = os.path.join(
                output_label_folder,
                label_file
            )

            with open(new_label_path, "w") as f:
                f.write("\n".join(new_labels) + "\n")

            processed += 1

    print(f"{split}: {processed} images copied")

# ==========================================
# 5. Create new data.yaml
# ==========================================

yaml_data = {
    "train": "../dataset_9class/train/images",
    "val": "../dataset_9class/valid/images",
    "test": "../dataset_9class/test/images",
    "nc": 9,
    "names": class_names
}

with open(
    os.path.join(OUTPUT, "data.yaml"),
    "w"
) as f:

    yaml.dump(
        yaml_data,
        f,
        sort_keys=False
    )

print()
print("===================================")
print("9-CLASS DATASET CREATED SUCCESSFULLY")
print("===================================")
print()
print("Location:")
print(OUTPUT)
print()
print("Classes:")

for i, name in enumerate(class_names):
    print(i, "->", name)