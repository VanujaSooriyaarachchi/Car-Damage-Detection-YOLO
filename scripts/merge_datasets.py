import os
import shutil

# Where the final merged dataset will live
MERGED_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\car_damage_yolo"

MERGED_IMG = os.path.join(MERGED_ROOT, "images")
MERGED_LAB = os.path.join(MERGED_ROOT, "labels")

# create target split folders
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(MERGED_IMG, split), exist_ok=True)
    os.makedirs(os.path.join(MERGED_LAB, split), exist_ok=True)

# All three datasets now share the same structure: train / valid / test
DATASETS = [
    {
        "name": "ds1",
        "root": r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset1",
    },
    {
        "name": "ds2",
        "root": r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset2",
    },
    {
        "name": "ds3",
        "root": r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO\data\dataset3",
    },
]


def merge_split(dataset, target_split):
    """
    Merge a single split (train/val/test) from one dataset into the merged dataset.
    Source split is:
        train -> train
        val   -> valid
        test  -> test
    """
    ds_name = dataset["name"]
    ds_root = dataset["root"]

    if target_split == "train":
        src_split = "train"
    elif target_split == "val":
        src_split = "valid"
    else:
        src_split = "test"

    src_img_dir = os.path.join(ds_root, src_split, "images")
    src_lab_dir = os.path.join(ds_root, src_split, "labels")

    if not os.path.isdir(src_img_dir) or not os.path.isdir(src_lab_dir):
        print(f"{ds_name}: No '{src_split}' split found. Skipping.")
        return

    dst_img_dir = os.path.join(MERGED_IMG, target_split)
    dst_lab_dir = os.path.join(MERGED_LAB, target_split)

    count = 0

    for fname in os.listdir(src_img_dir):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        stem, ext = os.path.splitext(fname)
        src_img_path = os.path.join(src_img_dir, fname)
        src_lab_path = os.path.join(src_lab_dir, stem + ".txt")

        if not os.path.exists(src_lab_path):
            # skip images without labels
            continue

        # Make filename unique by prefixing dataset name
        new_stem = f"{ds_name}_{stem}"
        dst_img_path = os.path.join(dst_img_dir, new_stem + ext)
        dst_lab_path = os.path.join(dst_lab_dir, new_stem + ".txt")

        shutil.copy2(src_img_path, dst_img_path)
        shutil.copy2(src_lab_path, dst_lab_path)
        count += 1

    print(f"{ds_name}: merged {count} images into {target_split}/")


if __name__ == "__main__":
    for split in ["train", "val", "test"]:
        print(f"\nMerging split: {split}")
        for ds in DATASETS:
            merge_split(ds, split)

    print("\nDone merging train / val / test into car_damage_yolo/")
