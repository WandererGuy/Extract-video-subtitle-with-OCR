"""
keep only image have the 1 line translation 
"""

from tqdm import tqdm

def is_int(text):
    try:
        int(text)
        return True
    except:
        return False
filepath = "VIETOCR_LOG_FILE_CHATGPT.txt"
filepath_refine = "VIETOCR_LOG_FILE_CHATGPT_REFINE.txt"
valid_lines = []
with open (filepath, "r", encoding = "utf-8") as f:
    lines = f.readlines()
    for index in tqdm(range(0,len(lines))):
        if index != len(lines) - 1:
            line = lines[index].strip()
            if ":" in line and ":"in lines[index+1]:
                valid_lines.append(line)
            else:
                continue
with open (filepath_refine, "w", encoding = "utf-8") as f:
    for line in tqdm(valid_lines, total=len(valid_lines)):
        f.write(line)
        f.write("\n")




vietocr_dataset_file = "VIETOCR_DATASET.txt"
with open(vietocr_dataset_file, "w", encoding = "utf-8") as f:
    pass
filepath_refine = "VIETOCR_LOG_FILE_CHATGPT_REFINE.txt"
dataset = {}
with open (filepath_refine, "r", encoding = "utf-8") as f:
    lines = f.readlines()
    for line in tqdm(lines, total=len(lines)):
        line = line.strip()
        image_name, ocr_output = line.split(":", 1)
        if is_int(ocr_output): # in case OCR gone wrong
            continue
        elif "text" in ocr_output or "image" in ocr_output:
            continue
        else:
            dataset[image_name] = ocr_output

for image_name, ocr_output in dataset.items():
    with open(vietocr_dataset_file, "a", encoding = "utf-8") as f:
        f.write(image_name)
        f.write("\t")
        f.write(ocr_output)
        f.write("\n")





import shutil 
import os
if os.path.exists("VIETOCR_DATASET_FOLDER"):
    shutil.rmtree("VIETOCR_DATASET_FOLDER")
vietocr_dataset_folder = "VIETOCR_DATASET_FOLDER"
os.makedirs(vietocr_dataset_folder, exist_ok = True)
fail_transfer = 0 
success_transfer = 0
for image_path in dataset.keys():
    try:
        shutil.copy(image_path, vietocr_dataset_folder)
        success_transfer += 1
    except:
        fail_transfer += 1
print (success_transfer)
print (fail_transfer)





t = []
with open(vietocr_dataset_file, "r", encoding = "utf-8") as f:
    lines = f.readlines()
    for line in lines:
        t.append(line.replace("save_video_frame_folder_all_crops", "VIETOCR_DATASET_FOLDER"))
with open(vietocr_dataset_file, "w", encoding = "utf-8") as f:
    for line in t:
        f.write(line)

"""
final output :
image in VIETOCR_DATASET_FOLDER
annotation in VIETOCR_DATASET.txt
"""
with open(vietocr_dataset_file, "r", encoding = "utf-8") as f:
    all_lines = f.readlines()
    num_dataset = len(all_lines)

# (1) Lấy k phần tử ngẫu nhiên (không lặp lại)
train_num = int(num_dataset * 0.8)
val_num = num_dataset - train_num
import random 
random.seed(42)
train_lines = random.sample(all_lines, train_num)

# (2) Tạo danh sách còn lại
val_lines = [x for x in all_lines if x not in train_lines]
with open ("VIETOCR_DATASET_TRAIN.txt", "w", encoding = "utf-8") as f:
    for line in train_lines:
        f.write(line)
with open ("VIETOCR_DATASET_VAL.txt", "w", encoding = "utf-8") as f:
    for line in val_lines:
        f.write(line)


"""
final result is image in VIETOCR_DATASET_FOLDER
train in VIETOCR_DATASET_TRAIN.txt
val in VIETOCR_DATASET_VAL.txt
"""