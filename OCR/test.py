t = []
with open ("VIETOCR_LOG_FILE.txt", "r", encoding = "utf-8") as f:
    lines = f.readlines()
    for line in lines:
        img_path = line.split(".jpg:", )[0]
        t.append(img_path + ".jpg")

import shutil 
import os 
os.makedirs("quan_ocr", exist_ok = True)
for filepath in t:
    shutil.copy(filepath, "quan_ocr")