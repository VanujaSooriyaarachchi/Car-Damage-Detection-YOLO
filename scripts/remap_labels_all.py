import os

# MASTER CLASS INDEX (final YOLO dataset)

# 0 dent
# 1 scratch
# 2 crack
# 3 glass shatter
# 4 lamp broken
# 5 tire flat
# 6 rust


def remap_labels(dataset_root, id_map, dataset_name="Dataset"):
    """
    Remap YOLO class IDs in label files according to id_map.
    Assumes the dataset has:
        dataset_root/train/labels
        dataset_root/valid/labels
        dataset_root/test/labels
    """
    print(f"\nRemapping labels for {dataset_name}")
    print(f"Dataset root: {dataset_root}")

    splits = ["train", "valid", "test"]

    for split in splits:
        labels_dir = os.path.join(dataset_root, split, "labels")
        if not os.path.isdir(labels_dir):
            print(f"Split '{split}' not found under {dataset_root}. Skipping.")
            continue

        print(f"Processing split: {split}")

        for fname in os.listdir(labels_dir):
            if not fname.endswith(".txt"):
                continue

            path = os.path.join(labels_dir, fname)

            with open(path, "r") as f:
                lines = f.read().strip().splitlines()

            new_lines = []
            for line in lines:
                parts = line.split()
                if len(parts) < 5:
                    continue  # invalid YOLO line

                old_id = int(parts[0])
                bbox = parts[1:]

                if old_id not in id_map:
                    print(f"WARNING: class {old_id} not in id_map for {fname}, skipping object.")
                    continue

                new_id = id_map[old_id]
                new_line = str(new_id) + " " + " ".join(bbox)
                new_lines.append(new_line)

            with open(path, "w") as f:
                if new_lines:
                    f.write("\n".join(new_lines) + "\n")
                else:
                    # leave empty if nothing valid remains
                    f.write("")

        print(f"Done split: {split}")

    print(f"Completed remapping for {dataset_name}\n")

# DATASET ROOTS 

# dataset1:
DATASET1_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset1"

# dataset2:
DATASET2_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset2"

# dataset3:
DATASET3_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset3"

# ID MAPPINGS FOR EACH DATASET

# Dataset1: ['crack', 'dent', 'glass shatter', 'lamp broken', 'scratch', 'tire flat']
id_map_dataset1 = {
    0: 2,  # crack         -> crack
    1: 0,  # dent          -> dent
    2: 3,  # glass shatter -> glass shatter
    3: 4,  # lamp broken   -> lamp broken
    4: 1,  # scratch       -> scratch
    5: 5,  # tire flat     -> tire flat
}

# Dataset2: ['dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat']
id_map_dataset2 = {
    0: 0,  # dent          -> dent
    1: 1,  # scratch       -> scratch
    2: 2,  # crack         -> crack
    3: 3,  # glass shatter -> glass shatter
    4: 4,  # lamp broken   -> lamp broken
    5: 5,  # tire flat     -> tire flat
}

# Dataset3: ['crack', 'dent', 'rust', 'scratch']
id_map_dataset3 = {
    0: 2,  # crack   -> crack
    1: 0,  # dent    -> dent
    2: 6,  # rust    -> rust
    3: 1,  # scratch -> scratch
}

# RUN REMAPPING

if __name__ == "__main__":
    remap_labels(DATASET1_ROOT, id_map_dataset1, dataset_name="Dataset 1")
    remap_labels(DATASET2_ROOT, id_map_dataset2, dataset_name="Dataset 2")
    remap_labels(DATASET3_ROOT, id_map_dataset3, dataset_name="Dataset 3")

    print("\nAll three datasets remapped to 7-class schema!")