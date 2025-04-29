from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

import os 
import cv2

def ocr(filepath, detector):
    filepath2 =  filepath
    img = Image.open(filepath2)
    # img = cv2.imread(filepath2)
    # img = cv2.copyMakeBorder(img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, None, value = 0) 
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = Image.fromarray(img) 
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




from fastapi import FastAPI, Form
import os 
import uvicorn
from change_ip import main as change_ip_main
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read(os.path.join('config','config.ini'))
host_ip = config['DEFAULT']['host'] 
port_num = "3061" 
script_name = "main_ocr"

app = FastAPI()
@app.get("/")
async def root():
    return {"detail":{"message": "Hello World"}}

detector = load_model()

@app.post("/ocr-inference")
async def ocr_inference(filepath: str = Form(...)):
    ocr_output = ocr(filepath, detector)
    VIETOCR_LOG_FILE = "VIETOCR_LOG_FILE.txt"
    with open(VIETOCR_LOG_FILE, "a", encoding = "utf-8") as f:
        f.write(filepath)
        f.write(":")
        f.write(ocr_output)
        f.write("\n")
        print (filepath)

    return {"result": ocr_output} # ocr_output
def main():
    change_ip_main()
    sleep(2)
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run(f"{script_name}:app", host=host_ip, port=int(port_num), reload=False, workers=1)

if __name__ == "__main__":
    main()


    