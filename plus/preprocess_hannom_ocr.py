import json 
import re
import numpy as np

input_file_path = "data/ocr/ocr_results.hannom.json"
output_file_path = "data/clean/TongTapVanHocVietNam06_clean.hannom.json"
cnt = 0

cleaned_ocr_data = []

with open(input_file_path, "r", encoding="utf-8") as input_file:
    ocr_data = json.load(input_file)

def is_chinese(text):
    hanzi_pattern = re.compile(r'[a-zA-Z0-9\*]')
    return bool(hanzi_pattern.search(text)) == 0

def sort_box(points):
    points = np.array(points)
    sorted_indices = np.lexsort((points[:, 0], points[:, 1]))
    top_two = points[sorted_indices[:2]]
    bottom_two = points[sorted_indices[2:]]

    top_two = top_two[np.argsort(top_two[:, 0])]
    top_left, top_right = top_two[0], top_two[1]

    bottom_two = bottom_two[np.argsort(bottom_two[:, 0])]
    bottom_left, bottom_right = bottom_two[0], bottom_two[1]

    return [top_left.tolist(), top_right.tolist(), bottom_right.tolist(), bottom_left.tolist()]

cnt = 0

def concatenate_data(ocr_data):
    global cnt
    for poem in ocr_data:
        file_name = poem["file_name"]
        data = poem["data"]
        tmp_data = data.copy()
        marked = []
        for item1 in tmp_data:
            if item1["text"] in marked:
                continue
            for item2 in tmp_data:
                if item1["text"] == item2["text"] or item2["text"] in marked:
                    continue
                if item1["position"][0][1] in range(item2["position"][0][1]-25, item2["position"][0][1]+25) :
                    if item1["position"][0][0] > item2["position"][0][0]:
                        data[data.index(item2)]["text"] = item2["text"] + item1["text"]
                        data[data.index(item2)]["position"][1] = item1["position"][1]
                        data[data.index(item2)]["position"][2] = item1["position"][2]
                        data.remove(item1)
                        marked.append(item2["text"])
                        marked.append(item1["text"])
                    else:
                        data[data.index(item1)]["text"] = item1["text"] + item2["text"]
                        data[data.index(item1)]["position"][1] = item2["position"][1]
                        data[data.index(item1)]["position"][2] = item2["position"][2]
                        data.remove(item2)
                        marked.append(item1["text"])
                        marked.append(item2["text"])
        cnt+=len(data)

for index, item in enumerate(ocr_data):
    file_name = item["file_name"]
    text_lines = item["data"]["text_lines"]
    data = []
    texts = []

    for text_line in text_lines:
        text = text_line["text"]
        position = text_line["position"]

        if is_chinese(text):
            cleaned_text = re.sub(r'[()]', '', text)
            texts.append(cleaned_text)
            data.append({
                "text": cleaned_text,
                "position": sort_box(position)
            })

    cleaned_ocr_data.append({"file_name": file_name, "data": data, "texts": texts})
    # cleaned_ocr_data.append({"file_name": file_name,  "texts": texts, "original_texts": item["data"]["texts"]})
    cnt += len(texts)

concatenate_data(cleaned_ocr_data)

with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(cleaned_ocr_data, output_file, ensure_ascii=False, indent=4)

print(f"[+] Saved cleaned OCR data to '{output_file_path.split('/')[-1]}'")
print(f"[+] Total number of lines: {cnt}")