from PIL import Image
import os
from pathlib import Path
from tkinter import filedialog
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from tensorflow.keras.models import load_model

# Tải lại mô hình đã lưu
img_height = 512
img_width = 512

model = load_model('festival_image_classification_v2.keras')
class_names = ['Bà Chúa Xứ','Đua Ghe Ngo','Giỗ Tổ Hùng Vương','Lễ hội chùa Hương','Lễ hội Đua Bò','Lễ hội Nghinh Ông','Lễ hội Thánh Gióng']
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

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # print(
    # "This image most likely belongs to {} with a {:.2f} percent confidence."
    # .format(class_names[np.argmax(score)], 100 * np.max(score))
    # )
    plt.imshow(img)
    plt.title(class_names[np.argmax(score)])
    plt.axis('off')
    plt.show()
    
    x = input("nhap 1 để dừng lại, nhập bất kì để tiếp tục")