from PIL import Image
import pytesseract
import os
import json
import cv2

folder_path = "data/images"
output_file_path = "data/ocr/ocr_results.quocngu.json"

def ocr_by_tesseract(image_path):
    raw_text = pytesseract.image_to_string(Image.open(image_path), lang='vie')
    print(f"Văn bản sau khi được OCR từ {image_path}:")
    print(raw_text[:100] + '...')
    return raw_text

def save_ocr_results_to_json(ocr_data, filename=output_file_path):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(ocr_data, json_file, ensure_ascii=False, indent=4)

def process_images_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]
    
    if not image_files:
        print("No image files found in the folder.")
        return

    ocr_data = {}

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"[+] Processing image: {image_file}")
        ocr_text = ocr_by_tesseract(image_path)
        ocr_data[image_file] = ocr_text

    save_ocr_results_to_json(ocr_data)

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

process_images_in_folder(folder_path)
