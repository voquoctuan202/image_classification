from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from tensorflow.keras.models import load_model
from pydantic import BaseModel

# Tải mô hình đã huấn luyện
model = load_model('festival_image_classification_v2.keras')
class_names = ['Bà Chúa Xứ','Đua Ghe Ngo','Giỗ Tổ Hùng Vương','Lễ hội chùa Hương','Lễ hội Đua Bò','Lễ hội Nghinh Ông','Lễ hội Thánh Gióng']
# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Định nghĩa dữ liệu đầu vào bằng Pydantic
class PredictionRequest(BaseModel):
    features: list

print(model.input_shape)

# Route cho API dự đoán
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
   
    # Đọc tệp hình ảnh dưới dạng nhị phân và chuyển đổi thành định dạng phù hợp với mô hình
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
     # Điều chỉnh kích thước và chuẩn hóa ảnh
    
    image = image.resize((180, 180))  # Điều chỉnh kích thước theo yêu cầu của mô hình
   
    # Dự đoán với mô hình
    
    try:
        
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0) 

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        
        
    except Exception as e:
        return {"error": str(e)}
    
    # Trả về kết quả dự đoán
    return {"prediction": class_names[np.argmax(score)], "score": float(100 * np.max(score)) }
    
    
        
# Route để phục vụ trang web
@app.get("/")
def serve_homepage():
    return FileResponse('static/index.html')

# Chạy ứng dụng FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
    
#uvicorn app:app --reload