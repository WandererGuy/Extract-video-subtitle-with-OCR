from openai import OpenAI

# load_from_json.py
import json

def load_config(path: str = "config.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

openai_config_path = "openai_config.json"
config = load_config()
secret_key = config["SECRET_KEY"]
print("Loaded secret key:", secret_key)
client = OpenAI(api_key = secret_key)

url_base = "https://11cb-2402-800-62d0-50a9-98e0-41d-9178-51f8.ngrok-free.app/"
image_parent_dir = "save_video_frame_folder_all_crops/"
url_base = url_base + image_parent_dir

def chatgpt_ocr(image_name):
    url = url_base + image_name
    print ("sending image url to chatgpt", url)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "what text is in this image, give me answer only"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url,
                        "detail":"low",
                    },
                },
            ],
        }],
    )

    return response.choices[0].message.content
import os
def extract_done_image ():
    with open ("VIETOCR_LOG_FILE_CHATGPT.txt", "r", encoding = "utf-8") as f:
        lines = f.readlines()

    done_image = []
    for line in lines:
        line = line.strip()
        if ":" in line:
            try:
                image_name, ocr_output = line.split(":",1)
                done_image.append(os.path.basename(image_name))
            except:
                pass
    return done_image

def fix_filepath(full_path):
    last_dir = os.path.basename(os.path.dirname(full_path))
    file_name = os.path.basename(full_path)

    result = f"{last_dir}\\{file_name}"
    return result


done_images_ls = extract_done_image()
folder = "save_video_frame_folder_all_crops"
import os 
for filename in sorted(os.listdir(folder)):
    if filename in done_images_ls:
        print ("------ already done ------")
        continue
    file_path = os.path.join(folder, filename)
    print ("----------------------------------------------------")
    ocr_output = chatgpt_ocr(filename)
    print ("filename", filename)
    try:
        print ("ocr_output", ocr_output)
    except:
        pass
    with open("VIETOCR_LOG_FILE_CHATGPT.txt", "a", encoding = "utf-8") as f:
        f.write(fix_filepath(file_path))
        f.write(":")
        f.write(ocr_output)
        f.write("\n")
