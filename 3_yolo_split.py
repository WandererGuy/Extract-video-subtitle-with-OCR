

import os
import shutil

def find_all_image_paths(folder_path: str) -> list[str]:
    # List of common video file extensions
    video_extensions = ['.jpg', '.png', '.jpeg']
    video_paths = []
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_paths.append(os.path.join(root, file))
    return video_paths

'''
after annotate in labelme 
we have folder ./images and ./labels
put them into a folder called yolo_dataset
this script will split the data into train, val
'''

folder_image = "yolo_dataset/images"
folder_label = "yolo_dataset/labels"
train_folder_image = "yolo_dataset_2/images/train"
train_folder_label = "yolo_dataset_2/labels/train"
val_folder_image = "yolo_dataset_2/images/val"
val_folder_label = "yolo_dataset_2/labels/val"

os.makedirs(train_folder_image, exist_ok=True)
os.makedirs(train_folder_label, exist_ok=True)

os.makedirs(val_folder_image, exist_ok=True)
os.makedirs(val_folder_label, exist_ok=True)

image_paths = find_all_image_paths(folder_image)
from sklearn.model_selection import train_test_split

# 2) First split: train vs. (validation + test)
train_paths, val_test_paths = train_test_split(
    image_paths,
    test_size=0.2,           # 20% goes to val+test
    random_state=42,         # for reproducibility
    shuffle=True
)
t = {}
for filepath in train_paths:
    filename = os.path.basename(filepath).split(".")[0]
    label_path = os.path.join(folder_label, filename) + ".txt"
    t[filepath.replace("\\", "/")] = label_path.replace("\\", "/")

v = {}
for filepath in val_test_paths:
    filename = os.path.basename(filepath).split(".")[0]
    label_path = os.path.join(folder_label, filename) + ".txt"
    v[filepath.replace("\\", "/")] = label_path.replace("\\", "/")

for filepath, label_path in t.items():
    shutil.copy(filepath, train_folder_image)
    shutil.copy(label_path, train_folder_label)

for filepath, label_path in v.items():
    shutil.copy(filepath, val_folder_image)
    shutil.copy(label_path, val_folder_label)