import cv2
import glob
import random
import yaml
import os

# ---------------------------------------
# 1. Load class names from data.yaml
# ---------------------------------------

with open("dataset/data.yaml", "r") as f:
    data = yaml.safe_load(f)

names = data["names"]

print("Number of classes:", len(names))


# ---------------------------------------
# 2. Find training images
# ---------------------------------------

images = glob.glob("dataset/train/images/*")

if not images:
    print("ERROR: No training images found!")
    exit()

# Select a random image
image_path = random.choice(images)

print("Selected image:", image_path)


# ---------------------------------------
# 3. Find corresponding label file
# ---------------------------------------

image_name = os.path.splitext(os.path.basename(image_path))[0]

label_path = os.path.join(
    "dataset/train/labels",
    image_name + ".txt"
)

if not os.path.exists(label_path):
    print("ERROR: Label file not found!")
    print(label_path)
    exit()


# ---------------------------------------
# 4. Read image
# ---------------------------------------

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read image!")
    exit()

height, width = image.shape[:2]


# ---------------------------------------
# 5. Read annotations
# ---------------------------------------

with open(label_path, "r") as f:
    labels = f.readlines()


print("\nClasses found in this image:")


# ---------------------------------------
# 6. Draw bounding boxes
# ---------------------------------------

for line in labels:

    parts = line.strip().split()

    if len(parts) != 5:
        continue

    class_id = int(parts[0])

    x_center = float(parts[1]) * width
    y_center = float(parts[2]) * height
    box_width = float(parts[3]) * width
    box_height = float(parts[4]) * height

    # Convert YOLO format to pixel coordinates
    x1 = int(x_center - box_width / 2)
    y1 = int(y_center - box_height / 2)

    x2 = int(x_center + box_width / 2)
    y2 = int(y_center + box_height / 2)

    # Get class name
    class_name = names[class_id]

    print(f"  {class_id} -> {class_name}")

    # Draw bounding box
    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    # Write class name
    cv2.putText(
        image,
        class_name,
        (x1, max(y1 - 10, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


# ---------------------------------------
# 7. Save preview
# ---------------------------------------

output_path = "test_images/dataset_preview.jpg"

cv2.imwrite(output_path, image)

print("\nDataset preview created successfully!")
print("Preview saved at:", output_path)