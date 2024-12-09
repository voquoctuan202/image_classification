#Setup
from PIL import Image
import os
from pathlib import Path
from tkinter import filedialog
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import PIL
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.metrics import Precision, Recall
from tensorflow.keras.models import Sequential
import seaborn as sns
import pathlib


    
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


#Hiển thị hình ảnh được thêm vào tập train


plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")
plt.show()

for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break


#Cải thiện hiệu suất của mô hình
AUTOTUNE = tf.data.AUTOTUNE


# train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

image_batch, labels_batch = next(iter(normalized_ds))

first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

#A basic Keras model
num_classes = len(class_names)


# Tăng cường dữ liệu (Data augmentation)
data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal", input_shape=(img_height,img_width,3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)

plt.figure(figsize=(10, 10))
for images, _ in train_ds.take(1):
  for i in range(9):
    augmented_images = data_augmentation(images)
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(augmented_images[0].numpy().astype("uint8"))
    plt.axis("off")
plt.show()    

#Xây dựng mô hình
model = Sequential([
  data_augmentation,
  layers.Rescaling(1./255),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes, name="outputs")
])
#Compile and train the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#Thông tin model
model.summary()

#==========================================================

#Train model with dropout, data_augmentation e10
epochs = 10
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

#Visualize training results
acc_10 = history.history['accuracy']
val_acc_10 = history.history['val_accuracy']

loss_10 = history.history['loss']
val_loss_10 = history.history['val_loss']

epochs_range = range(0,epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc_10, label='Training Accuracy')
plt.plot(epochs_range, val_acc_10, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss_10, label='Training Loss')
plt.plot(epochs_range, val_loss_10, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
model.save('model\\festival_image_classification_v11_e10.keras')

#==========================================================

#Train model with dropout, data_augmentation e20
epochs = 10
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

#Visualize training results

acc_20 = history.history['accuracy']
val_acc_20 = history.history['val_accuracy']

loss_20 = history.history['loss']
val_loss_20 = history.history['val_loss']

epochs_range = range(10,epochs+10)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc_20, label='Training Accuracy')
plt.plot(epochs_range, val_acc_20, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss_20, label='Training Loss')
plt.plot(epochs_range, val_loss_20, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
model.save('model\\festival_image_classification_v11_e20.keras')

#==========================================================

#Train model with dropout, data_augmentation e30
epochs = 10
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

#Visualize training results

acc_30 = history.history['accuracy']
val_acc_30 = history.history['val_accuracy']

loss_30 = history.history['loss']
val_loss_30 = history.history['val_loss']

epochs_range = range(20,epochs+20)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc_30, label='Training Accuracy')
plt.plot(epochs_range, val_acc_30, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss_30, label='Training Loss')
plt.plot(epochs_range, val_loss_30, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
model.save('model\\festival_image_classification_v11_e30.keras')

#==========================================================

#Train model with dropout, data_augmentation e40
epochs = 10
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

#Visualize training results

acc_40 = history.history['accuracy']
val_acc_40 = history.history['val_accuracy']

loss_40 = history.history['loss']
val_loss_40 = history.history['val_loss']

epochs_range = range(30,epochs+30)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc_40, label='Training Accuracy')
plt.plot(epochs_range, val_acc_40, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss_40, label='Training Loss')
plt.plot(epochs_range, val_loss_40, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
model.save('model\\festival_image_classification_v11_e40.keras')


#Hiển thị biểu đồ tổng    
acc = acc_10 + acc_20 + acc_30+ acc_40
val_acc = val_acc_10 + val_acc_20 + val_acc_30+ val_acc_40

loss = loss_10 + loss_20 + loss_30 + loss_40
val_loss = val_loss_10 + val_loss_20 + val_loss_30 + val_loss_40

epochs_range = range(40)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
