from PIL import Image
import os
from pathlib import Path
from tkinter import filedialog
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import joblib

# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential

from tensorflow.keras.models import load_model

# Tải lại mô hình đã lưu
img_height = 256
img_width = 256

model_cnn = load_model('model\\festival_image_classification_v11_e20.keras')
#Không thể sử dụng model KNN do lỗi: numpy.core._exceptions._ArrayMemoryError: Unable to allocate 15.2 GiB for an array with shape (2035286016,) and data type float64
#model_knn = joblib.load('model\\knn_model.pkl')
model_dtree =  joblib.load('model\\dtree_model.pkl')
model_rf = joblib.load('model\\rf_model.pkl')

class_names = ['Bà Chúa Xứ','Văn hóa chợ nổi Cái Răng','Chọi Trâu','Đờn ca Tài Tử Nam Bộ','Đua Ghe Ngo',
               'Giỗ Tổ Hùng Vương','Hội vật làng Sình Huế',
               'Lễ hội bánh dân gian Nam Bộ','Lễ hội chùa Hương',
               'Lễ hội đâm trâu Tây Nguyên ','Lễ hội Đua Bò','Lễ hội Nghinh Ông'
               ,'Lễ hội Thánh Gióng','Lễ hội Tháp Bà Ponagar','Nghề Đan Tre', 'Nghề Dệt Chiếu', 'Tết Trung Thu ở Hội An']
x=0



while (x!="1"):
    filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.jfif")]
    )
        

    img = tf.keras.utils.load_img(
    filepath, target_size=(img_height, img_width)
    )
    
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions_cnn = model_cnn.predict(img_array)
    score = tf.nn.softmax(predictions_cnn[0])

    img_2 = img.resize((200, 200))
    img_array = np.array(img_2)
    img_array = img_array.reshape(1, -1)
    #prediction_knn = model_knn.predict(img_array)
    prediction_dtree = model_dtree.predict(img_array)
    prediction_rf = model_rf.predict(img_array)
    

    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(img)
    plt.title("CNN:" + class_names[np.argmax(score)])
    plt.axis('off')
     
    # plt.subplot(2,2,2)
    # plt.imshow(img)
    # plt.title("KNN:" + str(prediction_knn))
    # plt.axis('off')
    
    plt.subplot(2,2,3)
    plt.imshow(img)
    plt.title("Decision Tree:" + str(prediction_dtree))
    plt.axis('off')
    
    plt.subplot(2,2,4)
    plt.imshow(img)
    plt.title("Random Forest:" + str(prediction_rf))
    plt.axis('off')

    plt.show()
    
    
    
    x = input("nhap 1 để dừng lại, nhập bất kì để tiếp tục")