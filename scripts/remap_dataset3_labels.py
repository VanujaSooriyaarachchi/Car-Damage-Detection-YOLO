import os

DATASET3_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset3"

splits = ["train", "valid", "test"]

# Mapping: old_id -> new_id
id_map = {
    0: 2,  # crack  -> 2
    1: 0,  # dent   -> 0
    2: 6,  # rust   -> 6
    3: 1   # scratch-> 1
}

for split in splits:
    labels_dir = os.path.join(DATASET3_ROOT, split, "labels")
    if not os.path.isdir(labels_dir):
        print(f"Labels dir not found for split '{split}': {labels_dir}")
        continue

    for fname in os.listdir(labels_dir):
        if not fname.endswith(".txt"):
            continue

        path = os.path.join(labels_dir, fname)

        with open(path, "r") as f:
            lines = f.read().strip().splitlines()

        new_lines = []
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            old_id = int(parts[0])
            if old_id not in id_map:
                print(f"WARNING: Unknown class id {old_id} in {path}")
                continue

            new_id = id_map[old_id]
            parts[0] = str(new_id)
            new_lines.append(" ".join(parts))

        with open(path, "w") as f:
            f.write("\n".join(new_lines))

print("Done remapping Dataset 3 labels.")