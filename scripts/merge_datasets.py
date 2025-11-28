import os
import shutil

PROJECT_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO"
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")

# Dataset roots
DS1_ROOT = os.path.join(DATA_ROOT, "dataset1")
DS2_ROOT = os.path.join(DATA_ROOT, "dataset2")
DS3_ROOT = os.path.join(DATA_ROOT, "dataset3")

# Output: combined pool
ALL_IMG_DIR = os.path.join(DATA_ROOT, "car_damage_all", "images")
ALL_LBL_DIR = os.path.join(DATA_ROOT, "car_damage_all", "labels")

os.makedirs(ALL_IMG_DIR, exist_ok=True)
os.makedirs(ALL_LBL_DIR, exist_ok=True)

print("ALL_IMG_DIR:", ALL_IMG_DIR)
print("ALL_LBL_DIR:", ALL_LBL_DIR)

# Helper to copy images+labels with a prefix
def copy_dataset(src_root, split_map, prefix):
    """
    src_root: path to datasetX root
    split_map: list of (split_name, src_split_folder_name)
       e.g. [("train", "train"), ("val", "valid"), ("test", "test")]
    prefix: string like "D1", "D2", "D3"
    """
    for logical_split, src_split_name in split_map:
        img_dir = os.path.join(src_root, src_split_name, "images")
        lbl_dir = os.path.join(src_root, src_split_name, "labels")

        if not os.path.isdir(img_dir):
            print(f"[{prefix}] WARNING: images dir not found: {img_dir}")
            continue
        if not os.path.isdir(lbl_dir):
            print(f"[{prefix}] WARNING: labels dir not found: {lbl_dir}")
            continue

        print(f"[{prefix}] Copying from split '{logical_split}' ({img_dir})")

        for fname in os.listdir(img_dir):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            base, ext = os.path.splitext(fname)
            img_src = os.path.join(img_dir, fname)
            lbl_src = os.path.join(lbl_dir, base + ".txt")

            if not os.path.exists(lbl_src):
                print(f"[{prefix}] WARNING: no label for {img_src}")
                continue

            # New base name with prefix & split for uniqueness
            new_base = f"{prefix}_{logical_split}_{base}"
            new_img_name = new_base + ext
            new_lbl_name = new_base + ".txt"

            shutil.copy2(img_src, os.path.join(ALL_IMG_DIR, new_img_name))
            shutil.copy2(lbl_src, os.path.join(ALL_LBL_DIR, new_lbl_name))

# Define split names for each dataset

# Dataset1 uses "train", "valid", "test"
DS1_SPLITS = [
    ("train", "train"),
    ("val",   "valid"),
    ("test",  "test"),
]

# Dataset2 uses "train", "val", "test"
DS2_SPLITS = [
    ("train", "train"),
    ("val",   "val"),
    ("test",  "test"),
]

# Dataset3 uses "train", "valid", "test"
DS3_SPLITS = [
    ("train", "train"),
    ("val",   "valid"),
    ("test",  "test"),
]

# Copy all three datasets into the combined pool
copy_dataset(DS1_ROOT, DS1_SPLITS, prefix="D1")
copy_dataset(DS2_ROOT, DS2_SPLITS, prefix="D2")
copy_dataset(DS3_ROOT, DS3_SPLITS, prefix="D3")

print("Total combined images:", len(os.listdir(ALL_IMG_DIR)))
print("Total combined labels:", len(os.listdir(ALL_LBL_DIR)))
