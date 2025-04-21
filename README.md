this repo takes a video with subtitle then make a ./ocr_mapping.yaml file which contain timestamp and transcription (aka subtitle), also with path to the segmented video
it uses video segment technique , transformer OCR and yolo
It is beneficial for speech2text making dataset given that video only have subtitle in frame instead of a timestamp or transcription.

# prepare
install ffmpeg from website
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install ultralytics
pip install fastapi uvicorn pydantic python-multipart
pip install ffmpeg-python
```

# usage 
open 2 server by 
```
python main_ocr
```
```
python main_yolo_ocr.py
```
then change path video in ./main_infer then 
```
python main_infer.py
```