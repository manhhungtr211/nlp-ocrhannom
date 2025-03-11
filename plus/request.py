import requests
import base64
import os
import json
from time import sleep
from natsort import natsorted

# Đường dẫn đến thư mục chứa ảnh và thư mục đầu ra
folder_path = "data/ocr/images"
api_url = "https://ocr.kandianguji.com/ocr_api"
output_file_path = "data/ocr_results.hannom.json"

# Tạo danh sách các file trong thư mục
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Lưu tất cả kết quả vào một danh sách
all_results = []

# Duyệt qua từng file ảnh
for file in files:
    
    print("[+] Processing file: {}".format(file))
    file_path = os.path.join(folder_path, file)

    # Đọc và mã hóa base64 nội dung ảnh
    with open(file_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Tạo payload cho API
    payload = {
        "token": "e9477578-b38d-4e7e-8ff9-e73aec68a6e3",  # Thay bằng mã thông báo API của bạn
        "email": "manhhung211.hcmus@gmail.com", 
        "image": image_base64,  # Ảnh được mã hóa base64
        "char_ocr": False,  # Không chỉ nhận dạng ký tự đơn lẻ
        "det_mode": "hp",  # Nhận dạng tự động kiểu bố cục
        "image_size": 0,  # Không thay đổi kích thước ảnh
        "return_position": True,  # Trả về thông tin tọa độ
        "return_choices": False,  # Không trả về danh sách các từ ứng cử viên
    }

    # Gửi yêu cầu POST
    response = requests.post(api_url, json=payload)

    # Xử lý phản hồi từ API
    if response.status_code == 200:
        result = response.json()
        if result["message"] == "success":
            result["file_name"] = file  # Thêm tên file vào kết quả
            all_results.append(result)  # Lưu kết quả vào danh sách tổng hợp
        else:
            print(f"[-] Error for file {file}: {result.get('info', 'Unknown error')}")
    else:
        print(f"[-] HTTP Error for file {file}: {response.status_code}")

# Sắp xếp kết quả theo tên file
all_results = natsorted(all_results, key=lambda x: x["file_name"])

# Lưu tất cả kết quả vào một tệp JSON tổng hợp
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(all_results, json_file, ensure_ascii=False, indent=4)
print(f"[+] All results saved to: {output_file_path}")
