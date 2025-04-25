from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

import os 
import cv2

def ocr(filepath, detector):
    img = cv2.imread(filepath)
    img = cv2.copyMakeBorder(img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, None, value = 0) 
    # You may need to convert the color.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
    img = Image.fromarray(img) 
    ocr_output = detector.predict(img)
    return ocr_output


def load_model():
    print ('************* start loading OCR model... *************')
    config = Cfg.load_config_from_name('vgg_transformer')
    config['weights'] = 'weights/vgg_transformer.pth'
    config['cnn']['pretrained']=False
    config['device'] = 'cuda:0'
    detector = Predictor(config)
    print ('************* model OCR loaded *************')

    return detector

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


def fix_filepath(full_path):
    last_dir = os.path.basename(os.path.dirname(full_path))
    file_name = os.path.basename(full_path)

    result = f"{last_dir}\\{file_name}"
    return result


detector = load_model()
VIETOCR_LOG_FILE = "VIETOCR_LOG_FILE.txt"
with open(VIETOCR_LOG_FILE, "w", encoding = "utf-8") as f:
    pass
folder_path = r"save_video_frame_folder_all_crops"
image_paths = find_all_image_paths(folder_path)
for file_path in image_paths:
    ocr_output = ocr(file_path, detector)
    with open(VIETOCR_LOG_FILE, "a", encoding = "utf-8") as f:
        f.write(fix_filepath(file_path))
        f.write(":")
        f.write(ocr_output)
        f.write("\n")
