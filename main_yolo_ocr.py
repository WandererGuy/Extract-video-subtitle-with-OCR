import os 
import cv2
import numpy as np
import torch 
print("CUDA is available:", torch.cuda.is_available())
import ultralytics
ultralytics.checks()
from ultralytics import YOLO

# model = YOLO("yolo11x-seg.pt")
model = YOLO("weights/best.pt")
# Assuming `model` is your PyTorch model
model.to('cuda')
import uuid
print('model on gpu' ,next(model.parameters()).is_cuda)

def inference(model, source_image, save_crop_folder):
    new_path_dict = {}
    batch_yolo_result = model.predict(conf=0.3, source=source_image, save=False)
    
    for single_image_result in batch_yolo_result:
        img = np.copy(single_image_result.orig_img)
        if len(single_image_result) == 0:
            return []

        for ci, single_object_result in enumerate(single_image_result):
            class_id = single_object_result.boxes.cls.tolist().pop()
            label = single_object_result.names[class_id]
            # get box confidence
            conf = single_object_result.boxes.conf.tolist().pop()
            # get box coordinate
            x1, y1, x2, y2 = single_object_result.boxes.xyxy.tolist()[0]
            # get crop image
            cropped_image = img[int(y1):int(y2), int(x1):int(x2)]
            new_path = os.path.join(save_crop_folder, str(uuid.uuid4()) + '.jpg')
            cv2.imwrite(new_path, cropped_image)
            new_path_dict[new_path] = y1
    # first to ocr is above line 
    sorted_new_path_dict = dict(sorted(new_path_dict.items(), key=lambda kv: kv[1]))
    print (sorted_new_path_dict)
    new_path_ls = sorted_new_path_dict.keys()
    return new_path_ls

import requests

def send_to_ocr(new_path_ls):
    frame_ocr = ""
    for path in new_path_ls:
        

        url = OCR_URL

        payload = {'filepath': path}
        files=[

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        json_response = response.json()
        result = json_response['result']
        frame_ocr += result + " "

    return frame_ocr.strip()

    

from fastapi import FastAPI, Form
import os 
import uvicorn
from change_ip import main as change_ip_main
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read(os.path.join('config','config.ini'))
host_ip = config['DEFAULT']['host'] 
OCR_URL = config['DEFAULT']['OCR_URL']
port_num = "3060"
script_name = "main_yolo_ocr"

app = FastAPI()
@app.get("/")
async def root():
    return {"detail":{"message": "Hello World"}}

@app.post("/yolo-ocr-inference")
async def yolo_ocr_inference(source_image: str = Form(...)):
    save_crop_folder = "crop_images"
    new_path_ls = inference(model, source_image, save_crop_folder)
    if new_path_ls == []:
        return {"result": ""}
    frame_ocr = send_to_ocr(new_path_ls)
    print (frame_ocr)
    return {"result": frame_ocr}
def main():
    change_ip_main()
    sleep(2)
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run(f"{script_name}:app", host=host_ip, port=int(port_num), reload=True, workers=1)

if __name__ == "__main__":
    main()


    
