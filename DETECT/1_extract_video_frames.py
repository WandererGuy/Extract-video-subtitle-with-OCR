import cv2
import os 
import uuid
import shutil 
import os
import time 
import yaml
import time 
from unidecode import unidecode
import yaml
from tqdm import tqdm

def start_video(video_path: str):
    video_capture = cv2.VideoCapture(video_path)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # Check if video is opened correctly
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        exit()
    return video_capture, total_frames

def calculate_capture_rate(total_frames: int, 
                           max_frame_count: int) -> int:
    num_capture_rate = int(total_frames / max_frame_count)        
    if num_capture_rate == 0:
        num_capture_rate = 1
    print ( "NUM CAPTURE RATE: " + str(num_capture_rate))
    return num_capture_rate


def process_video(video_capture, 
                  num_capture_rate: int,
                  max_frame_count:int, 
                  save_video_folder: str) -> None:
    frame_count = 0
    extracted_frame_count = 0
    while True:
        # Read the next frame
        ret, frame = video_capture.read()
        if not ret:
            break  # Exit loop when video ends
        if frame_count % num_capture_rate == 0:  # Capture every 4th frame
            # Save the frame as an image
            cv2.imwrite(os.path.join(save_video_folder, f'{extracted_frame_count}.jpg'), frame)
            print(f"Image extracted and saved as '{extracted_frame_count}.jpg'.")
            extracted_frame_count += 1
        frame_count += 1
        if extracted_frame_count >= max_frame_count:
            break
    # Release the video capture object
    video_capture.release()


def create_save_video_folder(output_folder: str, 
                             video_path:str) -> str:
    t = unidecode(os.path.basename(video_path).split(".")[0]).replace('"', '').replace("'", '')
    save_video_folder_name = str(uuid.uuid4())
    save_video_folder = os.path.join(output_folder, save_video_folder_name)
    os.makedirs(save_video_folder, exist_ok=True)
    return save_video_folder

if __name__ == '__main__':
    dest_folder = "save_video_frame_folder"
    max_frame_count = 100
    source_folder = r"D:\WORK\Speech2text_dan_toc\all_video_dan_toc"
    for filename in os.listdir(source_folder):
        source_video = os.path.join(source_folder, filename)
        video_capture, total_frames = start_video(source_video)
        num_capture_rate = calculate_capture_rate(total_frames, max_frame_count)
        save_video_folder = create_save_video_folder(dest_folder, source_video)
        process_video(video_capture, num_capture_rate, max_frame_count, save_video_folder)