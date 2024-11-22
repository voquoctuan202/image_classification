#Setup
from PIL import Image
import os
from pathlib import Path
from tkinter import filedialog
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import PIL
from tensorflow.keras.models import load_model

from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.metrics import Precision, Recall
from tensorflow.keras.models import Sequential
import seaborn as sns
import pathlib

# Hàm hiển thị Confusion Matrix
def plot_confusion_matrix(y_true, y_pred, class_names):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()
    
    
# Đường dẫn tới thư mục huấn luyện
data_dir = pathlib.Path("F:\\Subjects\\festival_photos").with_suffix('')


# Thiết lập thông số huấn luyện
batch_size = 32  # Kích thước của một batch
img_height = 256  # Chiều cao ảnh
img_width = 256  #Chiều dài ảnh

# Đếm số lượng ảnh
image_count = len(list(data_dir.glob('*/*.png')))
print(image_count)

#Chia dữ liệu cho tập Train
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size,
  )

#Chia dữ liệu cho tập Test
val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size,
  )

# Hiển thị danh sách các class
class_names = train_ds.class_names
print(class_names)

model_10 = load_model('model\\festival_image_classification_v11_e10.keras')
model_20 = load_model('model\\festival_image_classification_v11_e20.keras')
model_30 = load_model('model\\festival_image_classification_v11_e30.keras')
model_40 = load_model('model\\festival_image_classification_v11_e40.keras')


#===============================================================================
#epoch =10
# Dự đoán nhãn trên tập validation
print("e10\n")
y_true = []
y_pred = []

# Lặp qua từng batch trong val_ds
for images, labels in val_ds:
    predictions = model_10.predict(images)  # Dự đoán
    predicted_labels = np.argmax(predictions, axis=1)  # Lấy nhãn dự đoán
    y_true.extend(labels.numpy())  # Thêm nhãn thực tế
    y_pred.extend(predicted_labels)  # Thêm nhãn dự đoán

# Chuyển y_true và y_pred thành mảng numpy
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Hiển thị classification_report
report = classification_report(
    y_true, 
    y_pred, 
    target_names=class_names,  # Gắn tên các lớp
    digits=2  # Hiển thị 4 chữ số thập phân
)
print("Classification Report:\n", report)

# Hiển thị ma trận nhầm lẫn (Confusion Matrix)
conf_matrix = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", conf_matrix)
plot_confusion_matrix(y_true, y_pred, class_names)

#===============================================================================
#epoch =20
# Dự đoán nhãn trên tập validation
print("e20\n")
y_true = []
y_pred = []

# Lặp qua từng batch trong val_ds
for images, labels in val_ds:
    predictions = model_20.predict(images)  # Dự đoán
    predicted_labels = np.argmax(predictions, axis=1)  # Lấy nhãn dự đoán
    y_true.extend(labels.numpy())  # Thêm nhãn thực tế
    y_pred.extend(predicted_labels)  # Thêm nhãn dự đoán

# Chuyển y_true và y_pred thành mảng numpy
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Hiển thị classification_report
report = classification_report(
    y_true, 
    y_pred, 
    target_names=class_names,  # Gắn tên các lớp
    digits=2  # Hiển thị 4 chữ số thập phân
)
print("Classification Report:\n", report)

# Hiển thị ma trận nhầm lẫn (Confusion Matrix)
conf_matrix = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", conf_matrix)
plot_confusion_matrix(y_true, y_pred, class_names)

#===============================================================================
#epoch =30
# Dự đoán nhãn trên tập validation
print("e30\n")
y_true = []
y_pred = []

# Lặp qua từng batch trong val_ds
for images, labels in val_ds:
    predictions = model_30.predict(images)  # Dự đoán
    predicted_labels = np.argmax(predictions, axis=1)  # Lấy nhãn dự đoán
    y_true.extend(labels.numpy())  # Thêm nhãn thực tế
    y_pred.extend(predicted_labels)  # Thêm nhãn dự đoán

# Chuyển y_true và y_pred thành mảng numpy
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Hiển thị classification_report
report = classification_report(
    y_true, 
    y_pred, 
    target_names=class_names,  # Gắn tên các lớp
    digits=2  # Hiển thị 4 chữ số thập phân
)
print("Classification Report:\n", report)

# Hiển thị ma trận nhầm lẫn (Confusion Matrix)
conf_matrix = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", conf_matrix)
plot_confusion_matrix(y_true, y_pred, class_names)

#===============================================================================
#epoch =40
# Dự đoán nhãn trên tập validation
print("e40\n")
y_true = []
y_pred = []

# Lặp qua từng batch trong val_ds
for images, labels in val_ds:
    predictions = model_40.predict(images)  # Dự đoán
    predicted_labels = np.argmax(predictions, axis=1)  # Lấy nhãn dự đoán
    y_true.extend(labels.numpy())  # Thêm nhãn thực tế
    y_pred.extend(predicted_labels)  # Thêm nhãn dự đoán

# Chuyển y_true và y_pred thành mảng numpy
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Hiển thị classification_report
report = classification_report(
    y_true, 
    y_pred, 
    target_names=class_names,  # Gắn tên các lớp
    digits=2  # Hiển thị 4 chữ số thập phân
)
print("Classification Report:\n", report)

# Hiển thị ma trận nhầm lẫn (Confusion Matrix)
conf_matrix = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", conf_matrix)
plot_confusion_matrix(y_true, y_pred, class_names)
