import cv2
import os
import requests
import unidecode
import unicodedata
import uuid
import subprocess
import os
import uuid
import Levenshtein
import pandas as pd
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read(os.path.join('config','config.ini'))

YOLO_OCR_URL = config['DEFAULT']['YOLO_OCR_URL']

OCR_MAPPING_FILE = "ocr_mapping.yaml"
# OUTPUT_LOG = "output.log"
TIME_SHIFT = 0.1 
STATIC_FOLDER = "static"
THRESHOLD_SIMILARITY = 0.7
BANG_XOA_DAU = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A"*17 + "D" + "E"*11 + "I"*5 + "O"*17 + "U"*11 + "Y"*5 + "a"*17 + "d" + "e"*11 + "i"*5 + "o"*17 + "u"*11 + "y"*5
)
# when detect different OCR output, 
# a new time break happen but shift backward 0.1 second so previous audio happen at t1 to t2-0.1
def calculate_similarity(s1, s2):
    dist = Levenshtein.distance(s1, s2)
    sim  = 1 - dist / max(len(s1), len(s2))
    print(f"Levenshtein distance = {dist}, similarity = {sim:.3f}")
    return sim



def xoa_dau(txt: str) -> str:
    """
    make vietnam text with no accent
    """
    if not unicodedata.is_normalized("NFC", txt):
        txt = unicodedata.normalize("NFC", txt)
    return txt.translate(BANG_XOA_DAU).lower()

def compare_ocr_output(ocr1, ocr2):
    s1 = xoa_dau(ocr1)
    s2 = xoa_dau(ocr2)
    if s1 == s2 == "":
        return True
    if calculate_similarity(s1, s2) > THRESHOLD_SIMILARITY:
        return True
    else:
        return False


def send_to_yolo_ocr(frame_path):

    url = YOLO_OCR_URL

    payload = {'source_image': frame_path}
    files=[

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    json_response = response.json()
    ocr_output = json_response['result']
    return ocr_output




# def create_excel(frames):
# # Build a list of dicts
#     data = [
#         {
#             'frame_index': f.frame_index,
#             'frame_time' : f.frame_time,
#             'frame_ocr'  : f.frame_ocr
#         }
#         for f in frames
#     ]

#     # Create the DataFrame
#     df = pd.DataFrame(data)
#     # Write to Excel
#     df.to_excel('output.xlsx',      # path (relative or absolute) & filename
#                 sheet_name='Sheet1',# optional: name of the Excel sheet
#                 index=False)        # optional: don’t write row indices

def run_ffmpeg(start_time, end_time, input_path, output_path):
    command = [
        'ffmpeg',
        '-ss', str(start_time),
        '-to', str(end_time),
        '-i', str(input_path),
        '-c', 'copy',
        str(output_path)
    ]
    # Use the standard call for Python 3.7+
    result = subprocess.run(command, check=True, capture_output=True, text=True)

def extract_frames_with_timestamps(video_path: str, skip: int = 15):
    """
    read frame every 15 frames
    send to yolo-ocr to ocr frame 
    get the frame time start and end based on ocr output 
    (similarity Levenshtein) ( ocr output switch have less similarity below threshold)
    ocr output switch means audio need to be break at this switch time (aka segment audio)
    segment audio (given start time, end time)
    mapping ocr output to audio segment 
    note that:
    this script segment video based on subtitle (aka ocr output)
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video FPS: {fps:.3f}")
    frame_folder = os.path.join("static", str(uuid.uuid4()))
    os.makedirs(frame_folder, exist_ok=True)

    frame_idx = 0
    saved_idx = 0
    last_ocr_output = ""
    last_timestamp_s = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # end of video

        # Only process every `skip`-th frame
        if frame_idx % skip == 0:
            # Timestamp (in seconds)
            timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp_s = timestamp_ms / 1000.0

            frame_path = os.path.join(frame_folder, f"frame_{saved_idx:04d}.jpg")
            cv2.imwrite(frame_path, frame)

            # your OCR/YOLO call
            ocr_output = send_to_yolo_ocr(frame_path)

            print("-------------------------------------")
            print(f"{frame_path} @ {timestamp_s:.3f}s → {ocr_output}")
            timestamp_s = round(timestamp_s, 2)
            if compare_ocr_output(ocr_output, last_ocr_output):
                pass
            else:
                temp_ocr = last_ocr_output
                last_ocr_output = ocr_output
                print ("------------ new audio segment here -------------")
                print ("segment from ", last_timestamp_s, "to", timestamp_s, "OCR represent time interval:", temp_ocr)
                output_path_segment = os.path.join(STATIC_FOLDER, str(uuid.uuid4()) + ".mp4")
                """
                cut video segment and save
                ocr output switch may be sooner when detected by this algorithm since i scan every 15 frames, so time shift is needed
                time shift makes video from 1.2 to 3.1 becomes 1.0 to 2.9 
                """
                run_ffmpeg(start_time = last_timestamp_s,
                        end_time = str(round(timestamp_s-TIME_SHIFT,2)), 
                        input_path = video_path, 
                        output_path = output_path_segment)
                # with open (OUTPUT_LOG, "a", encoding = "utf-8") as f:
                    # text = str(last_timestamp_s) +  "__" + str(round(timestamp_s-TIME_SHIFT,2)) + "__" + str(temp_ocr) + "\n"
                    # f.write(text)
                with open (OCR_MAPPING_FILE, "a", encoding = "utf-8") as f:
                    text = str(output_path_segment) + ":" + "\n" + \
                    "\t" + "- " + str(last_timestamp_s) +  "__" + str(round(timestamp_s-TIME_SHIFT,2)) + "\n" + \
                    "\t" + "- " + str(temp_ocr) + "\n"
                    f.write(text)
                last_timestamp_s = round(timestamp_s-TIME_SHIFT,2)
            saved_idx += 1

        frame_idx += 1

    cap.release()
    print("Done. Extracted", saved_idx, "frames.")






if __name__ == "__main__":
    video_path = r"D:\WORK\Speech2text_dan_toc\test\mong_10.mp4"
    extract_frames_with_timestamps(video_path)
