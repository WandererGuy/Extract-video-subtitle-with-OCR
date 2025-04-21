from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

import os 
import cv2

def ocr(detect_results_path, detector):
    ocr_output = []
    for filename2 in sorted(os.listdir(detect_results_path)):
        print (filename2)
        filepath2 =  os.path.join(detect_results_path, filename2)
        img = cv2.imread(filepath2)
        img = cv2.copyMakeBorder(img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, None, value = 0) 
        # You may need to convert the color.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
        img = Image.fromarray(img) 
        name = detector.predict(img)
        ocr_output.append(name) # name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
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

detector = load_model()
detect_results_path = r"D:\WORK\Speech2text_dan_toc\crop_images"
ocr_output = ocr(detect_results_path, detector)
for output in ocr_output:
    print (output)