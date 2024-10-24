let percent_scores
var num_class 
// Hàm chuyển đổi hình ảnh sang định dạng PNG
function convertImageToPng(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);

                // Chuyển đổi hình ảnh sang PNG
                canvas.toBlob(function(blob) {
                    resolve(blob);
                }, 'image/png');
            };
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}





// Xử lý sự kiện khi người dùng gửi form
document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Ngăn form gửi dữ liệu mặc định
    
    // Lấy tệp hình ảnh từ form
    const fileInput = document.getElementById('input-image');
    const originalFile = fileInput.files[0];

    // Chuyển đổi hình ảnh sang PNG
    const pngBlob = await convertImageToPng(originalFile);
    console.log(pngBlob)
    // Tạo form data và thêm hình ảnh PNG vào
    const formData = new FormData();
    formData.append('file', pngBlob, 'image.png');
    
    // Gửi yêu cầu POST đến API với tệp hình ảnh
    const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    });
    
    // Nhận kết quả từ API
    const result = await response.json();
    
    var div = document.getElementById("predict");
    div.style.display = "block"
    
    percent_scores = result.percent_scores;
    num_class = result.num_class; 
    console.log("Num class predict: "+ num_class)
    // Hiển thị kết quả trên trang web

    
    document.getElementById('result').innerText = 'Kết quả dự đoán: ' + result.prediction;
    document.getElementById('name_class').innerText = 'Một số hình ảnh của ' + result.prediction;
    document.getElementById('score').innerText = 'Phần trăm dự đoán: ' + result.score.toFixed(2) + "%";
    //document.getElementById('image_urls').innerText = 'Kết quả dự đoán: ' + result.image_urls; 
    //Hiển thị hình ảnh đã chọn
    const selectedImage = document.getElementById('selected-image');
   
    selectedImage.src = URL.createObjectURL(pngBlob);
    selectedImage.style.display = 'block';

    const gallery = document.getElementById('image-gallery');
    gallery.innerHTML = "";
    const imageUrls = result.image_urls;
    imageUrls.forEach((url) => {
        const img = document.createElement('img');
        img.src =  url;
        
        img.style.width = "200px";
        img.style.margin = "10px";
        gallery.appendChild(img);
    });

    
});

async function changePredict(){
    
    
    const response = await fetch(`/change_predict?percent_scores=${percent_scores}`, {method: "GET"});
    
    // Nhận kết quả từ API
    const result = await response.json();
    percent_scores = result.percent_scores;
    num_class = result.num_class 
    console.log("Num class change predict: "+ num_class)
    // Hiển thị kết quả trên trang web
    document.getElementById('result').innerText = 'Kết quả dự đoán: ' + result.prediction;
    document.getElementById('name_class').innerText = 'Một số hình ảnh của ' + result.prediction;
    document.getElementById('score').innerText = 'Phần trăm dự đoán: ' + result.score.toFixed(2) + "%";
    //document.getElementById('image_urls').innerText = 'Kết quả dự đoán: ' + result.image_urls; 
  

    const gallery = document.getElementById('image-gallery');
    gallery.innerHTML = "";
    const imageUrls = result.image_urls;
    imageUrls.forEach((url) => {
        const img = document.createElement('img');
        img.src =  url;
        console.log(url);
        img.style.width = "200px";
        img.style.margin = "10px";
        gallery.appendChild(img);
    });

}

// function showChatBot(){
//     var div = document.getElementById("chatbot");
//     div.style.display = "block"
//     var response = document.getElementById("response")
//     response.innerHTML =""
//     getQuestion();
// }

// function hideChatBot(){
//     var div = document.getElementById("chatbot");
//     div.style.display = "none"
// }

// async function getQuestion() {
//     console.log("Num class get question: "+ num_class)
//     const response = await fetch(`/get_question?num_class=${num_class}`, { method: "GET" });
//     const data = await response.json();
//     document.getElementById("question").innerHTML = "<h3>" + data.question + "</h3>";
    
//     const optionsDiv = document.getElementById("options");
//     optionsDiv.innerHTML = "";
//     data.options.forEach((option, index) => {
//         optionsDiv.innerHTML += `<input type="radio" name="option" value="${option}"> ${option}<br>`;
//     });
//     document.getElementById("submitBtn").style.display = "block";
// }

// async function sendAnswer() {
//     const selectedOption = document.querySelector('input[name="option"]:checked').value;
//     const response = await fetch("/submit_answer", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ answer: selectedOption, num : num_class})
//     });
//     const data = await response.json();
//     document.getElementById("response").innerHTML = "<p><strong>Phản hồi:</strong> " + data.response + "</p>";
//     document.getElementById("submitBtn").style.display = "none";
//     document.getElementById("question").innerHTML = "";
//     document.getElementById("options").innerHTML = "";
// }

const chatInput =  document.querySelector(".chat-input textarea")
const sendChatBtn = document.querySelector(".chat-input span")
const chatBox = document.querySelector(".chatbox")
const chatToggler = document.querySelector(".chatbot-toggler")
let userMessage

async function getApiKey() {
    const response = await fetch("/get_api_key");
    const data = await response.json();
    return data.API_KEY;
}

function showCheckBtn(){
    const div = document.getElementById('checkBtn')
    div.style.display="block"
}
function hideCheckBtn(){
    const div = document.getElementById('checkBtn')
    div.style.display="none"
}



getApiKey().then(apiKey => {
    const API_KEY  = apiKey
    // Sử dụng apiKey ở đây
    console.log(API_KEY)
    const generateRespone = (incomingChatLi) => {
        const API_URL = "https://api.openai.com/v1/chat/completions"
        messageElement = incomingChatLi.querySelector("p")
        
        const requestOption = {
            method : "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": userMessage
                    }
                ]
            })
        }
        
        fetch(API_URL, requestOption).then(res => res.json()).then(data => {
            messageElement.textContent = data.choices[0].message.content
        }).catch((err) => {
            messageElement.textContent = "Opps! Something went wrong. Please try again"
        }).finally(() => chatBox.scrollTo(0, chatBox.scrollHeight))
    
    }
    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li")
        chatLi.classList.add("chat", className)
        let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`
        chatLi.innerHTML = chatContent
        chatLi.querySelector("p").textContent = message
        return chatLi
    }
    const createChatImg = (img, className) => {
        console.log("createChatImg" +  img.name)
        const chatLi = document.createElement("li")
        chatLi.classList.add("chat", className)
        let chatContent = className === "outgoing" ? `<img src="${URL.createObjectURL(img)}" style="max-width: 300px; max-height:300px">` : `<span class="material-symbols-outlined">smart_toy</span><img src="${URL.createObjectURL(img)}" style="max-width: 300px; max-height:300px">`
        chatLi.innerHTML = chatContent
        
        return chatLi
    }
    const createChatGallery = (imageUrls) =>{
        const chatLi = document.createElement("li")
        chatLi.classList.add('chat', "incoming")
        
        chatLi.style.marginRight = "-25px"
        let chatContent =  `<span style="margin-bottom:100px" class="material-symbols-outlined">smart_toy</span>`
        chatLi.innerHTML = chatContent
        imageUrls.forEach((url) => {
            const img = document.createElement('img');
            img.src =  url;
            console.log(url);
            img.style.width = "140px";
            
            img.style.margin = "2px";
            chatLi.appendChild(img);
        });
        // let chatContent = ""
        // chatLi.innerHTML = chatContent
        return chatLi
    }


    
    
     
    const handleChat = () => {
        userMessage = chatInput.value.trim()
        if(!userMessage) return 
        chatInput.value = ""
        
        chatBox.append(createChatLi(userMessage, 'outgoing'))
        chatBox.scrollTo(0, chatBox.scrollHeight)
        setTimeout(() =>{
            const incomingChatLi = createChatLi("Thinking...", 'incoming')
            chatBox.append(incomingChatLi)
           
            chatBox.scrollTo(0, chatBox.scrollHeight)
            generateRespone(incomingChatLi)
        }, 600)
    }
    
    
    sendChatBtn.addEventListener('click', handleChat)
    chatToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"))
    
    
    document.getElementById('inputImg').addEventListener('change', async function(event) {
        const file = event.target.files[0]; // Lấy file đã upload
        chatBox.append(createChatImg(file, 'outgoing'))
        const pngBlob = await convertImageToPng(file)
        
        chatBox.scrollTo(0, chatBox.scrollHeight)
        // Tạo form data và thêm hình ảnh PNG vào
        const formData = new FormData();
        formData.append('file', pngBlob, 'image.png');
        
        // Gửi yêu cầu POST đến API với tệp hình ảnh
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData
        });
        
        // Nhận kết quả từ API
        const result = await response.json();
        percent_scores = result.percent_scores;
        num_class = result.num_class; 
        setTimeout(() =>{
            chatBox.append(createChatLi(`Hình ảnh có thể là: ${result.prediction}`, 'incoming'))
            chatBox.append(createChatLi(`Xác xuất dự đoán khoản ${result.score.toFixed(2)} %`, 'incoming'))
            chatBox.append(createChatLi("Dưới đây là một số hình ảnh có liên quan", 'incoming'))
            chatBox.append(createChatGallery(result.image_urls))
            
            chatBox.scrollTo(0, chatBox.scrollHeight)   
            showCheckBtn()
        }, 600)
        
   
    });

    document.getElementById("trueBtn").addEventListener('click', () =>{
        hideCheckBtn()
        chatBox.append(createChatLi("Có vẻ dự đoán là đúng", 'outgoing'))
        chatBox.append(createChatLi("Tuyệt! Hãy hỏi bất kì thông tin gì về lễ hội này", 'incoming'))
        chatBox.scrollTo(0, chatBox.scrollHeight)
    }) 
    
    document.getElementById("falseBtn").addEventListener('click', async () =>{

        hideCheckBtn()
        chatBox.append(createChatLi("Có vẻ chưa đúng, hãy dự đoán lại", 'outgoing'))
        chatBox.scrollTo(0, chatBox.scrollHeight)
        const response = await fetch(`/change_predict?percent_scores=${percent_scores}`, {method: "GET"});
        
        // Nhận kết quả từ API
        const result = await response.json();
        percent_scores = result.percent_scores;
        num_class = result.num_class 
        console.log(result.prediction)
        
    
        percent_scores = result.percent_scores;
        num_class = result.num_class; 
        setTimeout(() =>{
            chatBox.append(createChatLi(`Hình ảnh có thể là: ${result.prediction}`, 'incoming'))
            chatBox.append(createChatLi(`Xác xuất dự đoán khoản ${result.score.toFixed(2)} %`, 'incoming'))
            chatBox.append(createChatLi("Dưới đây là một số hình ảnh có liên quan", 'incoming'))
            chatBox.append(createChatGallery(result.image_urls))
            
            chatBox.scrollTo(0, chatBox.scrollHeight)   
            showCheckBtn()
        }, 600)
    })  
     


});












