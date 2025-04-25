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
    batch_yolo_result = model.predict(conf=0.2, source=source_image, save=False)
    for single_image_result in batch_yolo_result:

        img = np.copy(single_image_result.orig_img)
        for ci, single_object_result in enumerate(single_image_result):
            class_id = single_object_result.boxes.cls.tolist().pop()
            label = single_object_result.names[class_id]
            # get box confidence
            conf = single_object_result.boxes.conf.tolist().pop()
            # get box coordinate
            x1, y1, x2, y2 = single_object_result.boxes.xyxy.tolist()[0]
            # get crop image
            cropped_image = img[int(y1):int(y2), int(x1):int(x2)]
            
            cv2.imwrite(os.path.join(save_crop_folder, str(uuid.uuid4()) + '.jpg'), cropped_image)



if __name__ == '__main__':
    save_crop_folder = "crop_images"
    os.makedirs(save_crop_folder, exist_ok=True)
    source_image = r"D:\WORK\Speech2text_dan_toc\static\d78fa68d-347f-437d-9149-e0ffcc38f57e\frame_0250.jpg"
    inference(model, source_image, save_crop_folder)