import os
import random
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from tensorflow.keras.models import load_model
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import  JSONResponse
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
import os

load_dotenv()

question = {
    "1": ["Lễ vía Bà Chúa Xứ là gì?","Thời gian diễn ra lễ hội?",
          "Địa điểm tổ chức của lễ hội?","Nguồn gốc của Bà Chúa Xứ?",
          "Các lưu ý khi đi tham quan lễ vía?",],
    "2": ["Chợ nổi là gì?","Thời gian họp chợ?",
          "Địa điểm của chợ?","Một số lưu ý khi tham quan chợ nổi Cái Răng?",
          "Các lưu ý khi đi tham quan lễ vía?",],
    "3": ["Lễ hội Chọi Trâu là gì?","Thời gian diễn ra Chọi Trâu?"
          "Địa điểm tổ chức?","Các phần thi đấu lễ hội?"
          "Trâu chọi là loại trâu gì?","Các lưu ý khi đi xem chọi trâu?"],
    "4": ["Đờn Ca Tài Tử là gì?","Nguồn gốc của Đòn Ca Tài tử?",
          "Phạm vi hoạt động của Đờn Ca Tài Tử?","Các nhạc cụ được sử dụng là gì?",
          "Một số ca khúc thuộc thể loại đờn ca tài tử","Một số địa điểm tổ chức đờn ca tài tử?"],
    "5": ["Đua Ghe Ngo là gì?","Thời gian và địa điểm tổ chức?",
          "Ghe ngo là gì?", "Ý nghĩa của lễ hội?"],
    "6": ["Giỗ Tổ Hùng Vương là gì?","Thời gian diễn ra?",
          "Địa điểm tổ chức?","Lịch sử của ngày Giỗ Tổ Hùng Vương?",
          "Các hoạt động có trong lễ giỗ tổ?", "Các địa điểm có đền Hùng?"],
    "7": ["Hội vật làng Sình là gì?","Thời gian và địa điểm tổ chức?",
          "Ý nghĩa của lễ hội?", "Các hoạt động có trong hội vật?"],
    "8": ["Lễ hội bánh dân gian là gì?","Thời gian và địa điểm tổ chức?",
          "Ý nghĩa của lễ hội bánh dân gian?", "Mục đích của lễ hội bánh dân gian?",
          "Các hoạt động có trong lễ hội?"],
    "9": ["Lễ hội chùa Hương là gì?","Thời gian và địa điểm diễn ra lễ hội?",
          "Hoạt động khai hội tại chùa Hương?","Các lưu ý khi tham gia?"],
    "10": ["Lễ hội đâm trâu Tây Nguyên là gì?","Thời gian diễn ra?",
          "Địa điểm nào được tổ chức?","Nghi thức của lễ hội ra sao?"
          "Ý nghĩa khi tổ chức"],
    "11": ["Lễ hội Đua Bò là gì?","Thời gian và địa điểm diễn ra?",
           "Tổ chức lễ hội có gì?","Thể lệ của cuộc thi?",
           "Ý nghĩa của lễ hội đua bò?"],
    "12": ["Lễ hội Nghinh Ông là gì?","Thời gian diễn ra?",
           "Các địa điểm tổ chức?","Các hoạt động trong phần lễ?",
           "Các hoạt động trong phần hội?", "Ý nghĩa lễ hội?"],
    "13": ["Lễ hội Thánh Gióng là gì?","Thời gian tổ chức?",
           "Các địa điểm diễn ra lễ hội?","Thánh Gióng là ai?",
           "Ý nghĩa lịch sử của lễ hội?"],
    "14": ["Lễ hội tháp bà Ponager là gì?",
           "Địa điểm của tháp bà Ponagar ?","Bà Ponagar là ai?",
           "Lịch sử của tháp bà Ponagar?"],
    "15": ["Nghề Đan Tre là gì","Các vùng nổi tiếng với nghề đan tre?",
           "Các sản phẩm của nghề đan tre","Ứng dụng của các sản phẩm tre đan"],
    "16": ["Nghề Dệt Chiếu là gì?","Các vùng nổi tiếng với nghề dệt chiếu?"],
    "17": ["Tết Trung Thu ở Hội An là gì?","Thời gian diễn ra lễ trung thu",
           "Những điều đặc biệt của tết trung thu ở Hội An"],
}

# Tải mô hình đã huấn luyện 
model_cnn = load_model('festival_image_classification_v11_e20.keras') # Mô hình CNN

class_names = ['Bà Chúa Xứ','Văn hóa chợ nổi Cái Răng','Chọi Trâu','Đờn ca Tài Tử Nam Bộ','Đua Ghe Ngo',
               'Giỗ Tổ Hùng Vương','Hội vật làng Sình Huế',
               'Lễ hội bánh dân gian Nam Bộ','Lễ hội chùa Hương',
               'Lễ hội đâm trâu Tây Nguyên ','Lễ hội Đua Bò','Lễ hội Nghinh Ông'
               ,'Lễ hội Thánh Gióng','Lễ hội Tháp Bà Ponagar','Nghề Đan Tre', 'Nghề Dệt Chiếu', 'Tết Trung Thu ở Hội An']

current_question_index = 0

# Khởi tạo ứng dụng FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="F:\\Subjects\\LuanVan\\project\\static"), name="static")
# Định nghĩa dữ liệu đầu vào bằng Pydantic
class PredictionRequest(BaseModel):
    features: list

@app.get("/get_api_key")
def get_api_key():
    return {"API_KEY": os.getenv("API_KEY")}

# Route cho API dự đoán
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
   
    # Đọc tệp hình ảnh dưới dạng nhị phân và chuyển đổi thành định dạng phù hợp với mô hình
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
     # Điều chỉnh kích thước và chuẩn hóa ảnh
    
    image = image.resize((256, 256))  # Điều chỉnh kích thước theo yêu cầu của mô hình
   
    # Dự đoán với mô hình
    
    try:
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0) 

        predictions = model_cnn.predict(img_array)
        
        score = tf.nn.softmax(predictions[0])
        percent_scores = [round(float(s) * 100, 2) for s in score]
        # print(percent_scores)
        num_class = str(np.argmax(score)+1)     
       
    except Exception as e:
        return {"error": str(e)}
    print(np.argmax(score))
    print(num_class)
    
    # Tạo đường dẫn đến thư mục tương ứng với class dự đoán
    images_dir = os.path.join("F:\\Subjects\\LuanVan\\project\\static\\imgs", num_class)
    
     # Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(images_dir):
        return {"error": "Directory not found for predicted class"}
    
     # Lấy tất cả tệp ảnh từ thư mục và chọn ngẫu nhiên một số ảnh
    all_images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    # Lấy tối đa 5 ảnh ngẫu nhiên từ thư mục
    selected_images = random.sample(all_images, min(len(all_images), 5))
    
    # Tạo URL trả về các ảnh
    image_urls = [f"..\\static\\imgs\\{num_class}\\{img}" for img in selected_images]
    # Trả về kết quả dự đoán và danh sách ảnh
    return {
        "prediction": class_names[np.argmax(score)],
        "score": float(100 * np.max(score)),
        "percent_scores" : percent_scores,
        "image_urls": image_urls,
        "num_class": int(np.argmax(score))
    }

@app.get("/change_predict")
async def change_predict(percent_scores):
    print("change predict ok")
    
    list_percents = percent_scores.split(',')
    float_percents = [float(i) for i in list_percents] 
    
    try:
        print(float_percents)
        i = np.argmax(float_percents)
        float_percents[i] = -1
        print(float_percents)
        score = float_percents

        print(float_percents)
        num_class = str(np.argmax(score) + 1)
    except Exception as e:
        return {"error": str(e)}
    
    # Tạo đường dẫn đến thư mục tương ứng với class dự đoán
    images_dir = os.path.join("..\\static\\imgs", num_class)
    
     # Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(images_dir):
        return {"error": "Directory not found for predicted class"}
    
     # Lấy tất cả tệp ảnh từ thư mục và chọn ngẫu nhiên một số ảnh
    all_images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    # Lấy tối đa 5 ảnh ngẫu nhiên từ thư mục
    selected_images = random.sample(all_images, min(len(all_images), 5))
    
    # Tạo URL trả về các ảnh
    image_urls = [f"..\\static\\imgs\\{num_class}\\{img}" for img in selected_images]
    # Trả về kết quả dự đoán và danh sách ảnh
    
    print(class_names[np.argmax(score)])
    print(np.max(score))
    print(image_urls)
    return {
        "prediction": class_names[np.argmax(score)],
        "score":  np.max(score),
        "image_urls": image_urls,
        "percent_scores": float_percents,
        "num_class": int(np.argmax(score))
    }


@app.get("/get-questions/{id_ques}")
def get_questions(id_ques: str):
    questions = question.get(id_ques, [])
    return JSONResponse(content=questions)
   
       
# Route để phục vụ trang web
@app.get("/")
def serve_homepage():
    return FileResponse('static/index.html')


# Chạy ứng dụng FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
    
#uvicorn app:app --reload