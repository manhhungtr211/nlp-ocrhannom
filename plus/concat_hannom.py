import json

input_file_path = "data/clean/TongTapVanHocVietNam06_clean.hannom.json"
output_file_path = "data/clean/TongTapVanHocVietNam06_clean.hannom.json"

with open(input_file_path, "r", encoding="utf-8") as input_file:
    ocr_data = json.load(input_file)
def concatenate_data(ocr_data):
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
    return ocr_data

ocr_data = concatenate_data(ocr_data)
    
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(ocr_data, output_file, ensure_ascii=False, indent=4)
                