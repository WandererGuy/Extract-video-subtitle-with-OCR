from ultralytics import YOLO
import yaml
import os
# Load the YAML file
epoch_train = 100

PRETRAIN_MODEL_PATH = "yolo11n.pt"
YAML_FILE_PATH = r"dataset.yaml"
if __name__ == '__main__':
    model = YOLO(PRETRAIN_MODEL_PATH)  # load a pretrained model (recommended for training)
    import torch 
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print (device)
    model.to(device)

    results = model.train(data=YAML_FILE_PATH, epochs=epoch_train, imgsz=640, device=device, patience=50)
