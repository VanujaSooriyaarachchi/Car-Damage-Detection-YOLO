import os
import shutil
import random

PROJECT_ROOT = r"D:\IIT\4 th Year\Machine Vision\Course Work\Car-Damage-Detection-YOLO"
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")

ALL_IMG_DIR = os.path.join(DATA_ROOT, "car_damage_all", "images")
ALL_LBL_DIR = os.path.join(DATA_ROOT, "car_damage_all", "labels")

YOLO_ROOT = os.path.join(DATA_ROOT, "car_damage_yolo")

IMG_TRAIN = os.path.join(YOLO_ROOT, "images", "train")
IMG_VAL   = os.path.join(YOLO_ROOT, "images", "val")
IMG_TEST  = os.path.join(YOLO_ROOT, "images", "test")

LBL_TRAIN = os.path.join(YOLO_ROOT, "labels", "train")
LBL_VAL   = os.path.join(YOLO_ROOT, "labels", "val")
LBL_TEST  = os.path.join(YOLO_ROOT, "labels", "test")

for d in [IMG_TRAIN, IMG_VAL, IMG_TEST, LBL_TRAIN, LBL_VAL, LBL_TEST]:
    os.makedirs(d, exist_ok=True)

all_images = [f for f in os.listdir(ALL_IMG_DIR)
              if f.lower().endswith((".jpg", ".jpeg", ".png"))]

random.shuffle(all_images)

n_total = len(all_images)
n_train = int(0.7 * n_total)
n_val   = int(0.2 * n_total)
n_test  = n_total - n_train - n_val

train_files = all_images[:n_train]
val_files   = all_images[n_train:n_train + n_val]
test_files  = all_images[n_train + n_val:]

def copy_split(files, img_dst, lbl_dst):
    for img_name in files:
        base, ext = os.path.splitext(img_name)
        lbl_name = base + ".txt"

        img_src = os.path.join(ALL_IMG_DIR, img_name)
        lbl_src = os.path.join(ALL_LBL_DIR, lbl_name)

        if not os.path.exists(lbl_src):
            print(f"WARNING: missing label for {img_name}, skipping")
            continue

        shutil.copy2(img_src, os.path.join(img_dst, img_name))
        shutil.copy2(lbl_src, os.path.join(lbl_dst, lbl_name))

copy_split(train_files, IMG_TRAIN, LBL_TRAIN)
copy_split(val_files,   IMG_VAL,   LBL_VAL)
copy_split(test_files,  IMG_TEST,  LBL_TEST)

print("Train:", len(train_files), "Val:", len(val_files), "Test:", len(test_files))