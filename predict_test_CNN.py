import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
from PIL import Image




model_path = 'festival_image_classification_v11_e20.keras'
test_data_dir = 'F:\\Subjects\\LuanVan\\test'

# Load mô hình CNN
model = load_model(model_path)
class_names = ['Bà Chúa Xứ','Văn hóa chợ nổi Cái Răng','Chọi Trâu','Đờn ca tài tử Nam Bộ','Đua Ghe Ngo',
               'Giỗ Tổ Hùng Vương','Hội vật làng Sình Huế',
               'Lễ hội bánh dân gian Nam Bộ','Lễ hội Chùa Hương',
               'Lễ hội đâm trâu Tây Nguyên','Lễ hội đua Bò','Lễ hội Nghinh Ông'
               ,'Lễ hội Thánh Gióng','Lễ hội Tháp Bà Ponagar','Nghề đan tre', 'Nghề dệt chiếu', 'Tết Trung Thu ở Hội An']


d = 0
for subdir, _, files in os.walk(test_data_dir):
    print("===================================================================")
    print(subdir)
    for file in files:
        file_path = os.path.join(subdir, file)
        try:
            with Image.open(file_path) as img:
                img = img.resize((256, 256))
                img = img.convert("RGB")
                img_array = tf.keras.utils.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0) # Create a batch

                predictions_cnn = model.predict(img_array)
                score = tf.nn.softmax(predictions_cnn[0])
                
                if str(class_names[np.argmax(score)]) in subdir:
                    print("Kết quả:"+ class_names[np.argmax(score)] +" Đúng")
                    d= d+1
                else:
                    print("Kết quả: "+ class_names[np.argmax(score)] +" Sai")
        except Exception as e:
            print(f"Could not process {file_path}: {e}")
    
    print("===================================================================")


print("Số kết quả đúng" + str(d))
#e10 = 114
#e20 = 124
#e30 = 111
#e40 = 107