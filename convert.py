import os
from pathlib import Path
from unidecode import unidecode

import os
from PIL import Image

def rename_files_in_folder(folder_path):
    # Sử dụng os.walk để duyệt qua tất cả các thư mục và tệp trong thư mục gốc và các thư mục con
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Tạo đường dẫn đầy đủ của tệp hiện tại
            old_file_path = os.path.join(root, filename)
            
            # Loại bỏ dấu tiếng Việt khỏi tên tệp
            new_filename = unidecode(filename)
            new_file_path = os.path.join(root, new_filename)
            
            # Đổi tên tệp
            if old_file_path != new_file_path:
                os.rename(old_file_path, new_file_path)
                print(f'Đã đổi tên: {old_file_path} -> {new_file_path}')




# def convert_images_to_png(directory):
   
#     # Duyệt qua tất cả các tệp trong thư mục
#     for filename in os.listdir(directory):
#         if filename.lower().endswith(('.jpg', '.jpeg', '.bmp', '.gif', '.jfif', '.tiff')):  # Kiểm tra định dạng ảnh
#             img_path = os.path.join(directory, filename)
#             img = Image.open(img_path)
            
#             # Lấy tên tệp mà không có phần mở rộng
#             base_name = os.path.splitext(filename)[0]
#             new_filename = base_name + ".png"
#             new_img_path = os.path.join(directory, new_filename)
            
#             # Nếu tên tệp đã tồn tại, thêm số vào sau tên
#             count = 1
#             while os.path.exists(new_img_path):
#                 new_filename = f"{base_name}_{count}.png"
#                 new_img_path = os.path.join(directory, new_filename)
#                 count += 1
            
#             # Lưu ảnh với định dạng PNG
#             img.save(new_img_path, 'PNG')
        
#             print(f"Đã chuyển đổi {filename} thành {new_filename}")
            
#             # Xóa ảnh gốc
#             os.remove(img_path)


def convert_webp_to_png(source_dir):
    # Duyệt qua tất cả các tệp .webp trong thư mục và các thư mục con
    for filepath in Path(source_dir).rglob('*.webp'):
        try:
            # Mở ảnh .webp
            with Image.open(filepath) as img:
                # Đặt tên file mới với đuôi .png
                new_filepath = filepath.with_suffix('.png')

                # Nếu tên đã tồn tại, thêm hậu tố để tránh ghi đè
                counter = 1
                while new_filepath.exists():
                    new_filepath = filepath.with_stem(f"{filepath.stem}_{counter}").with_suffix('.png')
                    counter += 1

                # Lưu ảnh dưới định dạng PNG
                img.save(new_filepath, format='PNG')
                print(f"Đã chuyển đổi: {new_filepath}")

        except Exception as e:
            print(f"Lỗi khi chuyển đổi {filepath}: {e}")


def convert_images_to_png(directory):
    for filepath in Path(directory).rglob('*'):
        try:
            with Image.open(filepath) as img:
                if img.format not in ['JPEG', 'PNG', 'GIF', 'BMP']:
                    new_filepath = filepath.with_suffix('.png')
                    img.convert('RGB').save(new_filepath, format='PNG')
                    print(f"Đã chuyển {filepath} sang {new_filepath}")
        except Exception as e:
            print(f"Lỗi khi xử lý {filepath}: {e}")
            
# Đường dẫn tới thư mục chứa tệp cần đổi tên
folder_path = "F:\\Subjects\\festival_photos"
# rename_files_in_folder(folder_path)
convert_images_to_png(folder_path)
#convert_webp_to_png(folder_path)


        


