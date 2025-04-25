import os 
def find_all_image_paths(folder_path: str) -> list[str]:
    # List of common video file extensions
    image_extensions = ['.jpg', '.png', '.jpeg']
    image_paths = []
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))
    return image_paths

import uuid
source_folder = "save_video_frame_folder"
image_paths = find_all_image_paths(source_folder)
image_paths = set(image_paths)
import random 
random.seed(42)
"""
makes multiple folders , each have 100 images to import each into label studio
"""


def split_into_n(lst, n):
    # base size for each of the first n-1 chunks
    size = len(lst) // n
    chunks = []
    for i in range(n - 1):
        chunks.append(lst[i*size : (i+1)*size])
    # last chunk takes all remaining elements
    chunks.append(lst[(n-1)*size :])
    return chunks

num_image_to_annotate = 1000
image_per_folder_to_import = 100
annotate_ls = random.sample(image_paths, num_image_to_annotate)
import shutil 
from tqdm import tqdm
num_chunks = int(num_image_to_annotate/image_per_folder_to_import)
print ("num_chunks", num_chunks)
chunks = split_into_n(annotate_ls, num_chunks)
for i in range (len(chunks)):
    final_folder = "label_studio_import_dataset/annotate_" + str(i)
    os.makedirs(final_folder, exist_ok=True)
    for image_path in tqdm(chunks[i], total=len(chunks[i])):
         
        shutil.copy(image_path, final_folder)
        dest_path = f"{final_folder}/" + os.path.basename(image_path)
        os.rename (dest_path, os.path.join(final_folder,str(uuid.uuid4()) + ".jpg"))