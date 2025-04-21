source_folder = "save_video"
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
image_paths = find_all_image_paths(source_folder)
import random 
annotate_ls = random.sample(image_paths, 100)
import shutil 
final_folder = "annotate_4" 
os.makedirs(final_folder, exist_ok=True)
for image_path in annotate_ls:
    shutil.copy(image_path, final_folder)
    dest_path = f"{final_folder}/" + os.path.basename(image_path)
    os.rename (dest_path, os.path.join(final_folder,str(uuid.uuid4()) + ".jpg"))