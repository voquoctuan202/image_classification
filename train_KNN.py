import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import cv2
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt


class_names = ['Bà Chúa Xứ','Văn hóa chợ nổi Cái Răng','Chọi Trâu','Đờn ca Tài Tử Nam Bộ','Đua Ghe Ngo',
               'Giỗ Tổ Hùng Vương','Hội vật làng Sình Huế',
               'Lễ hội bánh dân gian Nam Bộ','Lễ hội chùa Hương',
               'Lễ hội đâm trâu Tây Nguyên ','Lễ hội Đua Bò','Lễ hội Nghinh Ông'
               ,'Lễ hội Thánh Gióng','Lễ hội Tháp Bà Ponagar','Nghề Đan Tre', 'Nghề Dệt Chiếu', 'Tết Trung Thu ở Hội An']
# Bước 1: Đọc ảnh từ folder và gán nhãn
def load_images_from_folder(folder_path, img_size=(256, 256)):
    X = []
    y = []
    classes = os.listdir(folder_path)  # Danh sách các thư mục con (nhãn)
    
    for label in classes:
        class_folder = os.path.join(folder_path, label)
        if os.path.isdir(class_folder):  # Chỉ xử lý nếu là thư mục
            for img_file in os.listdir(class_folder):
                img_path = os.path.join(class_folder, img_file)
                img = cv2.imread(img_path)  # Đọc ảnh bằng OpenCV
                if img is not None:
                    
                    img = cv2.resize(img, img_size)
                    X.append(img)
                    y.append(label)
    
    return np.array(X), np.array(y)

# Bước 2: Hiển thị một số ảnh mẫu
def show_sample_images(X, y, samples=5):
    for i in range(samples):
        img = X[i].reshape(256, 256, 3)
        plt.imshow(img.astype(np.uint8))
        plt.title(f"Label: {y[i]}")
        plt.show()

# Bước 3: Chuẩn bị dữ liệu
def preprocess_data(X, y, test_size=0.2):
    # Chia dữ liệu thành tập huấn luyện và tập kiểm thử
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Chuẩn hóa dữ liệu
    X_train = X_train / 255.0
    X_test = X_test / 255.0
    
    # Giảm số chiều của ảnh xuống 1D
    X_train = X_train.reshape((X_train.shape[0], -1))
    X_test = X_test.reshape((X_test.shape[0], -1))
    
    return X_train, X_test, y_train, y_test

# Bước 4: Xây dựng mô hình KNN
def train_knn(X_train, y_train, n_neighbors=5):
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)
    return knn



def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

# Hàm hiển thị Confusion Matrix
def plot_confusion_matrix(y_true, y_pred, class_names):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

# Hàm tính và in các tiêu chí đánh giá
def evaluate_model(y_true, y_pred, class_names):
    # Accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    
    # Precision, Recall, F1 Score
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    print(f"Precision (weighted): {precision:.2f}")
    print(f"Recall (weighted): {recall:.2f}")
    print(f"F1 Score (weighted): {f1:.2f}")
    
    # Confusion Matrix
    print("\nConfusion Matrix:")
    plot_confusion_matrix(y_true, y_pred, class_names)
    
    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

# Bước 6: Chạy chương trình
if __name__ == "__main__":
   
    folder_path = "F:\\Subjects\\festival_photos"
    
    # Tải dữ liệu từ folder
    X, y = load_images_from_folder(folder_path, img_size=(256, 256))
    
    # Hiển thị một số ảnh mẫu
    show_sample_images(X, y, samples=5)
    
    # Chuẩn bị dữ liệu
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    
    # Huấn luyện mô hình KNN
    print("Training KNN...")
    knn = train_knn(X_train, y_train, n_neighbors=3)
    print("Evaluating KNN...")
    # evaluate_model(knn, X_test, y_test)
    
    y_pred = knn.predict(X_test)
    evaluate_model(y_test, y_pred, class_names)
    save_model(knn,"model\\knn_model.pkl")
    
   