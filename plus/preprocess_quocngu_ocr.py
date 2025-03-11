import re
import json

input_file_path = "data/ocr/gemini_api_results.quocngu.json"
output_file_path = "data/clean/TongTapVanHocVietNam06_clean.quocngu.json"

def clean_text_with_re(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text).lower()
    text = re.sub(r'\s+', ' ', text).strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def process_header(header):
    header = re.sub(r'\n+', '\n', header)
    anotate = ""
    title = ""
    for part in header.split("\n"):
        if not part:
            continue
        if "(" in part:
            anotate = part
        else:
            title += part + " "
    
    return  clean_text_with_re(title), clean_text_with_re(anotate)

cleaned_ocr_data = []

with open(input_file_path, "r", encoding="utf-8") as input_file:
    ocr_data = json.load(input_file)

index = 0
phien_am = []
dich_nghia = []
texts = ""

for item in ocr_data:
    if item["file_name"].split("_page")[1].replace(".png","") in ["001","018","010","022","030","037"]:
        continue
    texts += item["text"] + "\n"

# texts = re.sub(r'\n+', '\n', texts)
texts = texts.split("Phiên âm:")

for text in texts:
    if "Dịch nghĩa" in text:
        phien_am = text.split("Dịch nghĩa:")[0]
        header_pa = ""
        start_pa = 0
        if "(" in phien_am:
            for x in phien_am.split("\n\n"):
                start_pa += 1
                if "(" in x:
                    header_pa += x
                    break
                header_pa += x + "\n"
        else:
            for x in phien_am.split("\n\n"):
                start_pa += 1
                if not x:
                    continue
                else:
                    header_pa += x
                    break
        
        content_pa = phien_am.split("\n\n")[start_pa:]
        content_pa = "\n".join(content_pa)
        
        header_dn = ""
        content_dn = []
        start_dn = 0
        for seq in text.split("Dịch nghĩa:")[1:]:
            if "Chưa có nội dung dịch nghĩa" in seq:
                continue
            else:
                if "(" in " ".join(seq.split("\n\n")[:3]):
                    for part in seq.split("\n\n"):
                        start_dn += 1
                        if "(" in part:
                            header_dn = part
                            break
                        header_dn += part + "\n"
                else:
                    for part in seq.split("\n\n"):
                        start_dn += 1
                        if not part:
                            continue
                        else:
                            header_dn = part
                            break
                
                temp_content_dn = "\n".join(seq.split("\n\n")[start_dn:])
                temp_content_dn = re.sub(r'\n+', '\n', temp_content_dn)
                temp_content_dn = temp_content_dn.split("\n")
                temp_content_dn = [x for x in temp_content_dn if x]
                done = True
                comma = False
                tmp = ""
                for part in temp_content_dn:
                    if part[-1] not in [".",",","!","?"]:
                        done = False
                        tmp += part + " "
                    else:
                        if done:
                            if part[-1] == "," and temp_content_dn.index(part) + 1 < len(temp_content_dn):
                                if temp_content_dn[temp_content_dn.index(part) + 1][0].islower():
                                    tmp += part + " "
                                    done = False
                                    continue
                                elif temp_content_dn[temp_content_dn.index(part) + 1][-1] == ",":
                                    tmp += part + " "
                                    done = False
                                    continue
                            content_dn.append(part)
                        else:
                            content_dn.append(tmp + part)
                            tmp = ""
                            done = True

                print("===============phien am======================")
                print(header_pa)
                print("+++++++++++++++++++++")
                print(content_pa)
                print("===============dich nghia======================")
                print(header_dn)
                print("+++++++++++++++++++++")
                print("\n".join(content_dn))

                
                # header_pa = re.sub(r'\n+', '\n', header_pa)
                title_pa, anotate_pa = process_header(header_pa)
                title_dn, anotate_dn = process_header(header_dn)
                header_dn = re.sub(r'\n+', '\n', header_dn)

                # Xử lý content_pa
                content_pa = [x.strip() for x in (re.sub(r'\n+', '\n', content_pa)).split("\n") if x.strip()]

                poem_list = []
                poem_list.extend([{
                    "phien_am": title_pa,
                    "dich_nghia": title_dn
                },{
                    "phien_am": anotate_pa,
                    "dich_nghia": anotate_dn
                }])
                for pa, dn in zip(content_pa, content_dn):
                    poem_list.extend([{
                        "phien_am": clean_text_with_re(pa),
                        "dich_nghia": clean_text_with_re(dn),
                    }])


        cleaned_ocr_data.append({"id": index + 1, "poem_content": poem_list})

        index += 1
    else:
        continue

with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(cleaned_ocr_data, output_file, ensure_ascii=False, indent=4)