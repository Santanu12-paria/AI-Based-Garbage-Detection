import os
from collections import Counter
import yaml

# Load class names
with open("dataset_9class/data.yaml", "r") as f:
    data = yaml.safe_load(f)

class_names = data["names"]

counter = Counter()

label_folder = "dataset_9class/train/labels"

for file in os.listdir(label_folder):

    if not file.endswith(".txt"):
        continue

    with open(os.path.join(label_folder, file), "r") as f:

        for line in f:
            parts = line.strip().split()

            if len(parts) == 5:
                class_id = int(parts[0])
                counter[class_id] += 1

print("\nTraining Class Distribution")
print("=" * 40)

for class_id, class_name in enumerate(class_names):

    print(
        f"{class_id:2d}  {class_name:20s} "
        f"{counter[class_id]}"
    )

print("=" * 40)
print("Total objects:", sum(counter.values()))