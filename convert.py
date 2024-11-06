import os
import re
import unicodedata
from PIL import Image

def convert_images_to_png(directory):
    # Duyệt qua tất cả các thư mục và tệp trong thư mục gốc
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            # Kiểm tra nếu tệp có phần mở rộng là ảnh, trừ .png (vì ta không cần chuyển đổi .png sang .png)
            if file_name.lower().endswith(('.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                # Đường dẫn đầy đủ của tệp cũ
                old_file_path = os.path.join(root, file_name)
                # Đường dẫn mới với phần mở rộng .png
                new_file_name = os.path.splitext(file_name)[0] + '.png'
                new_file_path = os.path.join(root, new_file_name)

                # Mở ảnh và lưu lại dưới định dạng PNG
                with Image.open(old_file_path) as img:
                    img = img.convert("RGBA")  # Chuyển ảnh sang RGBA để đảm bảo độ tương thích
                    img.save(new_file_path, "PNG")
                
                os.remove(old_file_path)
                
                print(f"Đã chuyển đổi: {old_file_path} -> {new_file_path}")

def remove_vietnamese_accents(text):
    # Chuyển đổi ký tự có dấu thành ký tự không dấu
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return str(text)

def rename_files_in_directory(directory):
    # Duyệt qua tất cả các thư mục và tệp trong thư mục gốc
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            # Lọc các tệp ảnh (có đuôi .jpg, .png, .jpeg)
            if re.search(r'\.(jpg|png|jpeg)$', file_name, re.IGNORECASE):
                # Tạo tên tệp mới không có dấu tiếng Việt
                new_file_name = remove_vietnamese_accents(file_name)
                # Tạo đường dẫn đầy đủ cho tên cũ và tên mới
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(root, new_file_name)
                
                # Đổi tên tệp nếu tên mới khác tên cũ
                if old_file_path != new_file_path:
                    os.rename(old_file_path, new_file_path)
                    print(f"Đã đổi tên: {old_file_path} -> {new_file_path}")

# Thay đổi đường dẫn thư mục gốc tại đây
directory_path = "F:\\Subjects\\video_festival"
#rename_files_in_directory(directory_path)
convert_images_to_png(directory_path)




        


