import os
import re
import unicodedata
from PIL import Image

def convert_images_to_png(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith(('.jpg', '.jpeg', '.bmp', '.gif', '.tiff','.webp')):
                
                old_file_path = os.path.join(root, file_name)
                new_file_name = os.path.splitext(file_name)[0] + '.png'
                new_file_path = os.path.join(root, new_file_name)

                with Image.open(old_file_path) as img:
                    img = img.convert("RGBA")  
                    img.save(new_file_path, "PNG")
                
                os.remove(old_file_path)
                
                print(f"Đã chuyển đổi: {old_file_path} -> {new_file_path}")

def remove_vietnamese_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return str(text)

def rename_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            
            if re.search(r'\.(jpg|png|jpeg)$', file_name, re.IGNORECASE):
                
                new_file_name = remove_vietnamese_accents(file_name)
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(root, new_file_name)
                
                if old_file_path != new_file_path:
                    os.rename(old_file_path, new_file_path)
                    print(f"Đã đổi tên: {old_file_path} -> {new_file_path}")

def convert_images_to_srgb(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            try:
                with Image.open(file_path) as img:
                    if 'icc_profile' in img.info:
                     img.save(file_path, icc_profile=None)
            except Exception as e:
                print(f"Could not process {file_path}: {e}")
                
directory_path = "F:\\Subjects\\video_festival\\HVLS"
#Đổi tên file nếu có tiếng Việt
rename_files_in_directory(directory_path)
#Convert ảnh về PNG
convert_images_to_png(directory_path)
#Fix cảnh báo kênh màu iccp
convert_images_to_srgb(directory_path)

        


