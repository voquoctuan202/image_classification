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
import joblib
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
import os

load_dotenv()





# Tải mô hình đã huấn luyện 
model_cnn = load_model('festival_image_classification_v8.keras') # Mô hình CNN

    

class_names = ['Bà Chúa Xứ','Chọi Trâu','Đua Ghe Ngo','Giỗ Tổ Hùng Vương','Lễ hội chùa Hương','Lễ hội Đua Bò','Lễ hội Nghinh Ông','Lễ hội Thánh Gióng']

questions = [
    {
        "question": "Thông tin về lễ hội Bà Chúa Xứ?", #https://mytour.vn/vi/blog/bai-viet/le-hoi-ba-chua-xu-su-kien-truyen-thong-dac-biet-tai-an-giang.html
        "options": ["Đây là lễ hội gì?",
                    "Thời gian tổ chức là lúc nào?", 
                    "Địa điểm diễn ra là ở đâu?", 
                    "Số lượng khách thăm quan hàng năm?",
                    "Nguồn gốc của lễ hội Bà Chúa Xứ?",
                    "Có những hoạt động gì ở lễ hội?",
                    "Khi tham gia cần phải lưu ý những gì?"],
        "answers": {
            "Đây là lễ hội gì?": "Lễ hội Bà Chúa Xứ là một lễ hội mang bản sắc dân tộc đậm nét, chứa đựng nhiều màu sắc địa phương Nam Bộ .Từ lâu đã trở thành một truyền thống, một thói quen văn hóa được duy trì qua nhiều thế hệ. Hàng năm, đến ngày vía Bà Châu Đốc, nhiều du khách phương xa và người dân địa phương lại có dịp hội tụ, cùng nhau cầu chúc nhiều may mắn và sức khỏe cho gia đình.",
            "Thời gian tổ chức là lúc nào?": "Lễ hội vía Bà Chúa Xứ Núi Sam diễn ra từ ngày 23-27/4 Âm lịch hàng năm. Năm 2001, Bộ Văn hóa, Thể thao và Du lịch chính thức công nhận lễ hội Bà Chúa Xứ An Giang là một trong những lễ hội quốc gia quan trọng.", 
            "Địa điểm diễn ra là ở đâu?": "Lễ hội Bà Chúa Xứ diễn ra tại miếu Bà Chúa Xứ Núi Sam, huyện Châu Đốc, tỉnh An Giang, là nguồn cảm hứng cho người theo đạo Phật. Ngay cả khi không diễn ra lễ hội, Miếu Bà Chúa Xứ Núi Sam vẫn thu hút đông đảo tín đồ với lòng thành kính thông qua những buổi cúng bái.", 
            "Số lượng khách thăm quan hàng năm?":"Vào các ngày mùng 4, 5 và 14, 15/ 1 (âm lịch), số lượng du khách có ngày lên đến 125.700 lượt khách",
            "Nguồn gốc của lễ hội Bà Chúa Xứ?":"Theo truyền thuyết, trong thời kỳ quân Xiêm xâm chiếm nước ta (1820-1825), họ phát hiện một tượng đá lớn trên đỉnh núi Sam. Cố gắng khiêng tượng xuống núi, nhưng tượng trở nên nặng trĩu, không thể di chuyển nữa. Sau khoảng thời gian, tượng Bà Chúa Xứ hiện lên trong giấc mơ của làng." 
                                                + "Bà tự xưng là Bà Chúa Xứ và yêu cầu làng xây miếu thờ và khiêng tượng xuống núi. Bà hứa sẽ bảo vệ làng khỏi xâm lược và mang lại mưa thuận gió hòa. Đây là câu chuyện liên quan trực tiếp đến nguồn gốc của lễ hội Bà Chúa Xứ An Giang. <br>"
                                                +"Nghe theo lời bà, cả làng đoàn kết để khiêng tượng xuống núi. Nhưng thậm chí những chàng trai mạnh nhất cũng không thể nâng được tượng. Lúc này, một cô gái tự xưng là Chúa Xứ Thánh Mẫu xuất hiện và nói rằng chỉ cần 9 cô gái đồng trinh mới có thể khiêng tượng.<br>"
                                                +"Quả nhiên, 9 cô gái đồng trinh thành công khiêng tượng. Khi đến chân núi, tượng trở nên nặng và không thể di chuyển. Dân làng hiểu rằng đó là vị trí Bà Chúa chọn để lập miếu thờ. Từ đó, mỗi năm, từ ngày 22-27/4 (Âm lịch), lễ hội Bà Chúa Xứ được tổ chức để kỷ niệm câu chuyện nguồn gốc này.<br>",
            "Có những hoạt động gì ở lễ hội?":"Lễ <br>"
                                               +"Lễ hội Bà Chúa Xứ An Giang với nhiều nghi thức quan trọng, bắt đầu từ việc rước tượng Bà từ đỉnh núi Sam về miếu thờ vào ngày 22/4. Đêm 23 và rạng sáng 24/4 là Lễ Tắm Bà, sự kiện đặc biệt dành cho 9 phụ nữ đồng trinh."
                                               +"Vào 15 giờ ngày 24/4, Lễ Thỉnh sắc thần ông Thoại Ngọc Hầu và 2 vị phu nhân sẽ diễn ra, với nghi thức của các bô lão làng và Ban quản trị lăng miếu. Đêm 25 và rạng sáng 26/4 của lễ hội, Lễ Xây chầu và Lễ Túc yết sẽ diễn ra với nghi thức cầu cho mưa thuận gió hòa, mùa màng bội thu, đất đai phì nhiêu, sức khỏe và hạnh phúc cho cộng đồng."
                                               + "Hội<br>"
                                               +"Sau khi được công nhận là Lễ hội Quốc gia từ năm 2001, lễ hội Bà Chúa Xứ An Giang được đầu tư và tổ chức sôi nổi hơn. Hội không chỉ giữ nguyên các phần lễ truyền thống mà còn tổ chức nhiều chương trình văn hóa đặc sắc, phản ánh đa dạng văn hóa của bốn dân tộc anh em Kinh, Hoa, Chăm, Khmer…"
                                               +"Trò chơi dân gian như kéo co, thả diều nghệ thuật, cờ tướng, chọi gà, đẩy gậy... đồng thời, lễ hội còn có những hoạt động văn hóa nghệ thuật như múa lân sư rồng, múa bóng rỗi, múa mâm thao... Tất cả diễn ra sôi nổi trong khuôn khổ lễ hội.",
            "Khi tham gia cần phải lưu ý những gì?":"Nếu bạn dự định tham gia Lễ hội Bà Chúa Xứ An Giang, hãy chú ý đến những điều sau để tránh gặp phải các tình huống không hay:<br>"
                                                    +"Do lễ hội thu hút đông đảo người tham gia, hãy bảo quản tài sản cẩn thận để tránh rủi ro mất mát.<br>"
                                                    +"Để an toàn, hạn chế mua nhang đèn và heo quay từ người bán dạo. Chọn mua từ cửa hàng uy tín.<br>"
                                                    +"Tránh nhận lộc từ người không quen để tránh tình huống khó khăn sau này.<br>"
                                                    +"Khi tham gia lễ hội, sử dụng máy ảnh để lưu giữ những khoảnh khắc đẹp. Camera sắc nét sẽ giúp bạn có những bức hình tuyệt vời.<br>"
        }
    },
    {
        "question": "Thông tin về lễ hội Chọi Trâu?",# https://vi.wikipedia.org/wiki/L%E1%BB%85_h%E1%BB%99i_ch%E1%BB%8Di_tr%C3%A2u_%C4%90%E1%BB%93_S%C6%A1n
        "options": ["Lễ hội diễn ra ở đâu?",         #https://tailieu.com/le-hoi-choi-trau-a59624.html#le_hoi_choi_trau_do_son_dien_ra_o_dau_vao_ngay_nao
                    "Thời gian diễn ra lễ hội?", 
                    "Diễn biến của lễ hội?", 
                    "Nguồn gốc lễ hội?",
                    "Nội dung tại lễ hội?"],
        "answers": {
            "Lễ hội diễn ra ở đâu?": "Lễ hội chọi trâu Đồ Sơn, còn gọi là đấu ngưu , là một tập tục cổ, có từ xa xưa, một lễ hội truyền thống của người dân vạn chài tại vùng biển Đồ Sơn, Hải Phòng",
            "Thời gian diễn ra lễ hội?": "Diễn ra vào ngày 9 tháng 8 Âm lịch hàng năm",
            "Diễn biến của lễ hội?": "Lễ hội chọi trâu có hai phần, phần lễ và phần hội đan xen. Từ ngày mùng một đầu tháng, các vị cao niên các làng có trâu chọi làm lễ tế thần Điểm Tước ở đình Tổng. Sau đó là lễ rước nước, gắn với tục tế Thủy Thần. Lọ nước thần mỗi năm thay một lần được từng làng mang về đình riêng.<br>"
                                    +"Tại đình làng, các chủ trâu cho trâu ra làm lễ Thành Hoàng, sau khi lễ thần, trâu chọi được gọi là \"Ông trâu\"."
                                    +"Sáng ngày chính hội, 9/8 âm lịch, khoảng 1 giờ sáng, chủ tế các làng làm lễ xin phép Thành Hoàng đưa trâu đi thi đấu. Khoảng 6 - 7 giờ sáng, tổ chức lễ rước \"ông trâu\" ra đấu trường. "
                                    +"Dẫn đầu đám rước là cơ ngũ phương, trống, chiêng, long đình, long kiệu, bát bửu. Người khiêng long đình, long kiệu, trống, chiêng… chít khăn đỏ, mặc áo đỏ viền vàng, thắt lưng và quấn cạp đỏ. Người gọi loa, hay dịch lao đội khăn xếp, mặc áo lương đen, thắt lưng bố hậu đỏ, quần trắng. "
                                    +"Theo sau là các bô lão, chức sắc và thứ tự các ông trâu (theo kết quả xếp hạng đấu loại), trên lưng được chùm một tấm vải đỏ, sừng quấn một dải lụa điều. Đi bên cạnh mỗi ông trâu có hai chàng trai tay cầm cờ đuôi nheo để múa. Lễ rước các \"ông trâu\" vào các xào xá rộn rã trong tiếng nhạc bát âm, cờ bay phất phới kèm theo tiếng cổ động của dân cư trong vùng... <br>"
                                    +"Khi ông trâu bước vào xào xá, tiếng trống, tiếng loa nổi lên dõng dạc, đổ hồi như tiếng sóng dội vào Hòn Độc, nơi trâu sẽ được hiến tế Thủy Thần.<br>"
                                    +"Tiếp theo là nghi thức múa cờ khai hội được 24 tráng niên của làng chia thành hai hàng trình diễn vừa uyển chuyển, vừa mạnh mẽ, màu sắc biến hoá linh hoạt và huyền ảo trong những âm thanh của trống, thanh la; tái hiện lại lễ ra quân của Quận He Nguyễn Hữu Cầu trước giờ xuất trận; thể hiện ước nguyện cầu mong Thần Gió phù hộ cho thuyền bè cưỡi sóng vượt ra ngoài biển khơi.<br>"
                                    +"Múa cờ vừa dứt, từ hai phía hai \"ông trâu\" được dẫn vào xới, có người che lọng và múa cờ hai bên. Khi hai \"ông trâu\" cách nhau 20 m, người dắt nhanh chóng rút \"sẹo\" cho trâu rồi khẩn trương thoát ra ngoài sới chọi. Hai ông trâu hoàn toàn tự do lao vào chọi nhanh giành thắng bại.<br>"
                                    +"Kết thúc lễ hội, ông trâu thắng cuộc được làm lễ rước trở về. Sáng ngày 10 tháng 8, toàn bộ ông trâu tham gia lễ hội được đem giết thịt làm lễ vật tế thần ở đình, có kèm theo một đĩa đựng tiết và lông trâu (mao huyết). Khoảng 12 giờ trưa lễ tế bắt đầu. Sau đó, đĩa mao huyết được đổ xuống biển, phần còn lại được chia lộc thần cho dân với niềm tin một vụ khai thái mới bình an, nhiều tôm cá.<br>"
                                    +"Vào ngày 16 tháng 8, làng tiến hành nghi thức \"tống thần\" và rã đám, kết thúc lễ hội.",
            "Nguồn gốc lễ hội?": "Cho đến nay, chưa xác định chính xác lịch sử hình thành lễ hội. Cộng đồng địa phương còn lưu truyền nhiều câu chuyện, truyền thuyết về lễ hội như sau:<br>"
                                +"1. \"Ở chân núi Đồ Sơn, huyện Nghi Dương, có đền thờ Thủy Thần. Tương truyền có người bán thổ đi qua, thấy hai con trâu chọi nhau dưới đền, nên hàng năm đến ngày 9 tháng 8, có tục chọi trâu để tế thần\" (Theo sách Đại Nam nhất thống chí)<br>"
                                +"2. Lịch sử lễ hội chọi trâu gắn với huyền thoại về một cô thôn nữ xinh đẹp tên là Đế, do có thai với vua Thủy Tề, bị dân làng phạt vạ, quan lại địa phương mang cô ra biển dìm. Cô gái oan ức, hiển linh, cộng đồng địa phương lập đề thờ, tên gọi đền Bà Đế. Linh thiêng, nơi bà chết, tôm cá kéo đến tập trung, năm này qua năm khác, các vạn chài kéo đến đánh cá. Về sau, cộng đồng địa phương tổ chức Lễ hội chọi Trâu, những con trâu thắng mang ra biển cúng tế Bà Chúa. Cũng có ý kiến cho rằng, truyền thuyết dìm chết nàng Đế ở ngoài khơi Hòn Độc là di vết của tục hiến sinh các cô gái cho Thủy Thần có từ thời kỳ nguyên thủy đến thời sơ kỳ phong kiến; về sau, khi trình độ xã hội phát triển, việc hiến sinh con vật được thay thế.<br>"
                                +"3. Cũng ở nơi đây, cộng đồng dân cư Đồ Sơn còn lưu truyền sự tích về người hùng áo vải, Quận He Nguyễn Hữu Cầu người làng Lôi Động xã Tân An, huyện Thanh Hà, vì cuộc sống ấm no của người dân vạn chài đã phất cờ chống lại phong kiến thối nát tàn bạo thời kỳ 1741 – 1751. Tưởng nhớ công đức Người, hàng năm nhân dân Đồ Sơn mở hội chọi Trâu, múa cờ. Cũng có tài liệu cho rằng: \"Mỗi khi đánh trận thắng ông thường mổ trâu khao quân. Những con trâu chọi mổ bụng dứt dây lao ra, chọi nhau quyết liệt. Quân sĩ thấy thế hứng khởi reo hò vang dội. Kể từ đó, hàng năm, Nguyễn Hữu Cầu mở hội chọi trâu để cổ vũ động viên tinh thần quân sĩ\".<br>",
            "Nội dung tại lễ hội?":"Chọn, nuôi và huấn luyện trâu <br>"
                                +"Để chuẩn bị người nuôi trâu đã phải lựa chọn rất công phu,tỉ mỉ trong việc tìm và nuôi dưỡng trâu, chăm sóc kĩ lưỡng trong khoảng một năm. Thông thường thì sau Tết Nguyên đán, các sới chọi đều cử người có nhiều kinh nghiệm đi khắp nơi để mua trâu, có khi họ phải lặn lội hàng tháng trời vào các tỉnh Thanh Hóa, Nghệ An, Nam Định, Thái Bình, thậm chí lên tận Tuyên Quang, Bắc Kạn... mới tìm được con trâu vừa ý"
                                +"Trâu phải là những con trâu đực khỏe mạnh, da đồng, lông móc, một khoang bốn khoáy, hàm đen, tóc tráp (lông trên đầu cứng, dày để tránh nắng), có ức rộng, cổ tròn dài và hơi thu nhỏ về phía đầu, lưng càng dày, càng phẳng có khả năng chống chịu được đòn của đối phương.... là trâu gan. Háng trâu phải rộng nhưng thu nhỏ về phía hậu càng nhọn càng quý. Sừng trâu phải đen như mun, đầu sừng vênh lên như hai cánh cung, giữa hai sừng có túm tóc hình chóp trên đỉnh đầu là khoáy tròn,hai sừng phải nhọn. Mắt trâu phải đen, tròng đỏ."
                                +"Trường đấu<br>"
                                +"Trường đấu, hay sân chọi thường là những bãi đất rộng, khoảng 805 x 1002 m, có hào nước bao quanh. Phía trong hào có hai dáy lán làm chỗ đứng cho trâu chọi gọi là \"xào xá\". Ngoài ra, xung quanh có khán đài để mọi người quan sát và cổ vũ trâu thi đấu.",
        }
    },
    {
        "question": "Thông tin về lễ hội Đua Ghe Ngo?",
        "options": ["Thời gian tổ chức?", 
                    "Địa điểm tổ chức?", 
                    "Nguồn gốc lễ hội?", 
                    "Ghe Ngo là gì?",
                    "Quá trình tham gia như thế nào?",
                    "Ý nghĩa của lễ hội?"],
        "answers": {
            "Thời gian tổ chức?": "Thường được tổ chức trong tháng 10 Âm lịch hàng năm",
            "Địa điểm tổ chức?": "Được tổ chức tại Sóc Trăng, với sự tham gia của nhiều đội đua đến từ các tỉnh như: Trà Vinh, Kiên Giang, Hậu Giang, Cà Mau, Cần Thơ, An Giang",
            "Nguồn gốc lễ hội?": "Đua ghe Ngo - một trò chơi thể thao dân tộc Khmer, bao giờ cũng gắn với nghi lễ cúng trăng - đút cốm dẹp (Óoc Om Bóc), bởi khi thu hoạch mùa lúa mới, đồng bào Khmer thường làm lễ cúng tạ ơn các vị thần mặt trăng, thần đất, thần nước đã phù hộ ban cho mưa thuận gió hòa, mùa màng tươi tốt nên bà con thu hoạch được mùa. Trải qua nhiều thế kỷ hình thành và phát triển, Đua ghe Ngo được người Khmer gọi là Bon Pro-năng Tuk Ngô (Hội đua ghe Ngo) và được tổ chức vào dịp lễ cúng trăng - đút cốm dẹp, nên được gọi chung là Lễ hội Óoc Om Bóc - Đua ghe Ngo, tiếng Khmer gọi là “Pithi Bon Oóc Om Bóc - Pro-năng Tuk Ngô”<br>."
                                +" Khi nói về sự tích của chiếc ghe Ngo, thật ra chiếc ghe này ngày xưa không phải là những chiếc ghe để dành cho cuộc đua như ngày hôm nay, mà là những chiếc ghe được sử dụng làm phương tiện vận chuyển quân chính quy phòng khi có chiến tranh xảy ra của lãnh chúa cai quản vùng xứ sở Ba Sắc ngày xưa.",
            "Ghe Ngo là gì?": "Ghe ngo ngày xưa là một chiếc thuyền độc mộc, làm từ một thân cây khoét ruột. Ngày nay, việc tìm thân cây sao vừa to vừa dài để đóng ghe rất khó khăn, nên người Khmer làm ghe ngo bằng cách ghép những mảnh ván với nhau. <br>"
                            +"Ghe ngo được làm gần giống hình con rắn, dài khoảng từ 25 đến 30m, ở giữa chỗ rộng nhất là 1,1m, đầu được uốn cong lên như hình đầu rắn, đuôi (sau lái) cũng được uốn cong lên nhưng cao hơn phía đầu một chút.<br>"
                            +"Người ta đóng từ 24 đến 27 cây thanh ngang trên chiếc ghe, để vừa cho hai người ngồi. Mỗi ghe làm phải đảm bảo cho từ 40 đến 60 người ngồi bơi và chỉ huy. Dù cho ghe có bao nhiêu vận động viên, nhưng luôn luôn có ba người điều khiển, một người ngồi mũi chuyên về chỉ đạo tâm linh của ghe đua, tổ chức lễ cúng xuống ghe, chỉ huy toàn ghe, điều khiển kỹ thuật bơi của ghe đua; một người ngồi giữa và một người ngồi đuôi giữ nhiệm vụ thổi còi để thúc giục và điều chỉnh kỹ thuật bơi của các vận động viên.<br>"
                            +"Mỗi chiếc ghe có một biểu tượng riêng. Việc chọn biểu tượng ghe Ngo liên quan đến địa danh, hay quan niệm truyền thống của mỗi chùa. Biểu tượng ghe đại diện cho một tổ chức, thể hiện quyền uy của chiếc ghe, chẳng những là dấu hiệu để ghi nhớ mà còn bộc lộ sức mạnh của ghe đua. Thông thường, biểu tượng của ghe ngo là các con vật có sức mạnh, hoặc có khả năng chạy nhanh…<br>",
        
            "Ý nghĩa của lễ hội?":"Đua ghe ngo đã trở thành lễ hội lớn và cũng là sản phẩm du lịch của tỉnh Sóc Trăng. Tại địa điểm đua, người ta xây dựng thành hai khán đài dài (A, B) và lớn sức chứa lên đến vài nghìn người và rất dễ quan sát cuộc đua. Đặc biệt, người Khmer rất hăm hở chờ đợi được chứng kiến đội đua của mình để cổ vũ động viên và sẽ rất tự hào nếu ghe mình có giải cao.<br>"
                                +"Đua ghe ngo ngày nay trở thành ngày hội chung của 3 dân tộc Kinh-Khmer-Hoa, làm cho mối quan hệ cộng đồng các tộc người ở miền Tây Nam Bộ ngày càng gắn kết.<br>"
                                +"Đồng bào Khmer Sóc Trăng tổ chức lễ hội đua ghe Ngo như một phong tục tốt đẹp, một ngày hội lớn để mọi người vui chơi, tranh đua tài nghệ, sức mạnh với nhau, là một nét đặc trưng văn hóa của vùng sông nước miền Tây xứng đáng được bảo tồn<br>",
        }
    },
    {
        "question": "Thông tin về Giỗ Tổ Hùng Vương?",
        "options": ["Giỗ Tổ Hùng Vương là gì?", 
                    "Hùng Vương là ai?", 
                    "Thời gian diễn ra?", 
                    "Địa điểm tổ chức?",
                    "Các hoạt động nào được diễn ra?",
                    "Ý nghĩa lịch sử?"
                    ],
        "answers": { #https://vi.wikipedia.org/wiki/Gi%E1%BB%97_T%E1%BB%95_H%C3%B9ng_V%C6%B0%C6%A1ng
            "Giỗ Tổ Hùng Vương là gì?":"Ngày Giỗ Tổ Hùng Vương hay còn gọi là Lễ hội Đền Hùng hoặc tôn xưng là ngày Quốc giỗ là một ngày lễ của Việt Nam. Đây là ngày hội truyền thống của Người Việt tưởng nhớ công lao dựng nước của Hùng Vương.", 
            "Hùng Vương là ai?":"Hùng Vương là cách gọi các vị vua nước Văn Lang của người Lạc Việt. Hùng Vương thứ I là con trai của Lạc Long Quân, lên ngôi vào năm 2879 trước công nguyên, đặt quốc hiệu là Văn Lang, chia nước làm 15 bộ, truyền đời đến năm 258 trước công nguyên", 
            "Thời gian diễn ra?":"Diễn ra vào ngày 10 tháng 3 Âm lịch hằng năm", 
            "Địa điểm tổ chức?":"Được diễn ra ở nhiều nơi trên khắp đất nước Việt Nam, nhưng lễ lớn nhất được tổ chức là Đền Hùng ở Việt Trì, Phú Thọ ",
            "Các hoạt động nào được diễn ra?":"Hoạt động chính trong lễ Giỗ Tổ:<br>"
                                            +"Lễ dâng hương: Đây là nghi thức quan trọng nhất, với sự tham gia của các lãnh đạo quốc gia, người dân địa phương và du khách. Nghi lễ này nhằm thể hiện lòng thành kính, cầu mong quốc thái dân an, mưa thuận gió hòa, đất nước thịnh vượng.<br>"
                                            +"Lễ hội và các hoạt động văn hóa: Bên cạnh nghi lễ dâng hương, lễ hội còn có các hoạt động văn hóa nghệ thuật, trò chơi dân gian như hát xoan, múa sạp, đánh đu, thi gói bánh chưng bánh dày - tượng trưng cho truyền thống lâu đời của dân tộc.",
            "Ý nghĩa lịch sử?":"Vua Hùng là những vị vua đầu tiên trong lịch sử Việt Nam, lập nên nhà nước Văn Lang - nhà nước sơ khai của người Việt, cách đây khoảng 4000 năm.<br> Lễ Giỗ Tổ Hùng Vương thể hiện lòng biết ơn của người dân Việt Nam đối với tổ tiên, và thể hiện tình đoàn kết dân tộc. Câu nói \"Dù ai đi ngược về xuôi, nhớ ngày Giỗ Tổ mùng mười tháng ba\" đã trở thành một truyền thống ăn sâu trong tâm thức người Việt."
        }
    },
    {
        "question": "Thông tin về lễ hội Chùa Hương?",
        "options": ["Thời gian diễn ra?", "Địa điểm diễn ra?", "Ý nghĩa lễ hội?", "Các hoạt động có trong lễ hội?" ],
        "answers": {
            "Thời gian diễn ra?":"Lễ hội Chùa Hương chính thức khai mạc vào ngày mùng 6 tháng Giêng âm lịch và thường kéo dài đến hết tháng 3 âm lịch. Tuy nhiên, thời điểm đông đúc nhất là trong những ngày đầu năm mới, đặc biệt là dịp Tết Nguyên đán.", 
            "Địa điểm diễn ra?":"Lễ hội diễn ra tại quần thể Chùa Hương (hay còn gọi là Hương Sơn), thuộc xã Hương Sơn, huyện Mỹ Đức, thành phố Hà Nội. Chùa Hương không chỉ là một điểm đến hành hương tâm linh mà còn là danh thắng nổi tiếng với cảnh đẹp thiên nhiên hùng vĩ, với núi non, sông suối hữu tình.<br>"
                                +"Trong quần thể này có nhiều ngôi chùa, đền, động khác nhau, nhưng trung tâm là Chùa Thiên Trù và Động Hương Tích - nơi được mệnh danh là \"Nam Thiên Đệ Nhất Động\".", 
            "Ý nghĩa lễ hội?":"Lễ hội Chùa Hương là lễ hội phật giáo lớn, được tổ chức nhằm tôn vinh Đức Phật Bà Quan Thế Âm Bồ Tát, cầu cho quốc thái dân an, mưa thuận gió hòa, và đồng thời cầu mong bình an, tài lộc cho bản thân và gia đình.<br>"
                            +"Đây cũng là dịp để du khách thưởng ngoạn cảnh sắc thiên nhiên tuyệt đẹp, thả mình vào không gian thanh tịnh của Phật giáo.", 
            "Các hoạt động có trong lễ hội?":"Lễ dâng hương: Nghi lễ tôn giáo quan trọng nhất trong Lễ hội Chùa Hương là lễ dâng hương tại các ngôi chùa, đền, động. Người dân đến đây để cầu may mắn, bình an cho gia đình, công việc thuận lợi và sức khỏe dồi dào.<br>"
                                            +"Hành hương: Du khách thường phải đi qua dòng suối Yến thơ mộng bằng thuyền để vào khu vực chùa. Sau đó, họ leo núi để đến với Động Hương Tích, nơi được xem là điểm tâm linh chính yếu của chuyến hành hương.<br>"
                                            +"Hoạt động văn hóa, văn nghệ: Ngoài các nghi lễ tôn giáo, lễ hội còn có nhiều hoạt động văn hóa như hát chèo, hát văn, hát quan họ, và các trò chơi dân gian.<br>" 
        }
    },
    {
        "question": "Thông tin về lễ hội Đua Bò?",
        "options": ["Thời gian tổ chức?", "Địa điểm tổ chức?", "Ý nghĩa của lễ hội", "Các hoạt động chính có trong lễ hội?"],
        "answers": {
            "Thời gian tổ chức?":"Lễ hội Đua Bò 7 Núi thường được tổ chức vào dịp Tết Trung Thu (rằm tháng Tám âm lịch), thu hút đông đảo người dân và du khách tham gia. Năm 2024, lễ hội này sẽ diễn ra vào ngày 17/9 dương lịch.", 
            "Địa điểm tổ chức?":"Lễ hội được tổ chức tại khu vực Bảy Núi, thuộc tỉnh An Giang, một khu vực nổi tiếng với nhiều ngọn núi, phong cảnh thiên nhiên hùng vĩ.", 
            "Ý nghĩa của lễ hội": "Lễ hội Đua Bò không chỉ đơn thuần là một cuộc thi mà còn thể hiện sự gắn kết, tình đoàn kết của các dân tộc trong vùng, cũng như thể hiện sức mạnh và tinh thần thể thao của người dân nơi đây.<br>"
                                +"Đây cũng là dịp để người dân bày tỏ lòng biết ơn đối với những thành quả lao động, cầu mong mùa màng bội thu.<br>", 
            "Các hoạt động chính có trong lễ hội?":"Đua Bò: Cuộc đua bò được tổ chức tại các bãi cỏ rộng, nơi các chú bò đã được huấn luyện kỹ lưỡng sẽ thi tài tốc độ. Người điều khiển sẽ dùng dây cương dẫn dắt bò, và bò nào về đích trước sẽ là người chiến thắng.<br>"
                                                +"Biểu diễn văn nghệ: Lễ hội thường có các tiết mục biểu diễn văn nghệ truyền thống của các dân tộc tại chỗ, như múa lân, hát dân ca, và các điệu múa truyền thống.<br>"
                                                +"Trò chơi dân gian: Ngoài đua bò, lễ hội còn có nhiều hoạt động trò chơi dân gian thú vị, tạo không khí vui tươi cho sự kiện.<br>"
        }
    },
    { #https://langchaixua.com/du-lich-mui-ne/le-hoi-nghinh-ong-vung-bien/#Le_hoi_Nghinh_Ong_la_gi
        "question": "Thông tin về lễ hội NGhinh Ông?",
        "options": ["Lễ hội Nghinh Ông là gì?", "Nguồn gốc của lễ hội?", "Địa điểm diễn ra?", "Thời gian tổ chức?", "Quá trình diễn ra gồm những gì?","Ý nghĩa lễ hội"],
        "answers": {
            "Lễ hội Nghinh Ông là gì?":"Lễ hội nghinh Ông là lễ hội nước lớn nhất của người dân miền biển. Lễ hội còn có nhiều tên gọi khác như: lễ rước cốt ông, lễ tế cá “Ông”, lễ cầu ngư, lễ nghinh “Ông”, lễ cúng “Ông”, lễ nghinh ông Thủy tướng,… Mặc dù mang nhiều tên gọi khác nhau nhưng tất cả đều mang chung một quan niệm rằng cá “Ông” là một sinh vật linh thiêng ở biển, là vị cứu tinh của họ mỗi lúc tàu, thuyền của họ gặp nạn trên biển.", 
            "Nguồn gốc của lễ hội?":"Theo lịch sử thì Lễ hội Nghinh Ông cùng Tục thờ Cá Ông có nguồn gốc xuất phát từ tục thờ Cá Ông của người Chăm. Được du nhập vào Việt Nam từ rất sớm, trải qua sự bản địa hóa, tục thờ cá Ông trở thành tín ngưỡng của người Việt và cả người Hoa.<br>"
                                    +"Theo truyền thuyết thì vào những ngày đầu lập quốc, Nguyễn Ánh trong một lần bị quân Tây Sơn truy đuổi, thủy quân của Nguyễn Ánh tháo chạy ra biển thì gặp phải sóng to gió lớn. Trong lúc nguy khốn không biết làm cách nào thì bỗng có một con cá Ông to lớn ghé đưa thuyền vào bờ.<br>"
                                    +"Về sau, khi thắng được quân Tây Sơn và lên ngôi vua, Nguyễn Ánh nhớ ơn cứu mạng đã phong tặng  cá Ông là Nam Hải Đại Tướng quân và cho dân lập miếu thờ cúng cá Ông…” <br>", 
            "Địa điểm diễn ra?":"Lễ hội Nghinh Ông được tổ chức vào các thời gian khác nhau, tùy vào từng nơi sẽ có thời gian tổ chức riêng: Ở Vũng Tàu lễ thường được tổ chức vào ngày 15/8 – 18/8 âm lịch hàng năm tại Khu di tích đình thần Thắng Tam thuộc phường 2, Tp. Vũng Tàu. Ở Cà Mau lễ hội được tổ chức trong 3 ngày 14, 15, 16 tháng 2 âm lịch hàng năm tại cửa sông Ông Đốc, huyện Trần Văn Thời.<br>"
                                +"Ở Tiền Giang được tổ chức vào 2 ngày mùng 9 và mùng 10 tháng 3 Âm lịch tại Đình Thần xã Kiểng Phước. Tại Cà Mau thì lễ được tổ chức vào ngày 14, 15, 16 tháng 2 âm lịch hàng năm tại cửa sông Ông Đốc, huyện Trần Văn Thời, tỉnh Cà Mau. Ở Cần Giờ người dân tổ chức lễ hội  hàng năm từ 14-17/8 âm lịch. Còn tại Khánh Hòa lễ sẽ bắt đầu vào ngày 15 tháng 12 âm lịch, ….<br>", 
            
            "Quá trình diễn ra gồm những gì?":"Lễ hội Nghinh Ông dù được tổ chức ở địa phương nào thì cũng sẽ có 2 phần bắt buộc là phần lễ và phần hội. Phần lễ sẽ bao gồm lễ tế và lễ rước kiệu của Nam hải Tướng quân xuống thuyền rồng ra biển. Sau phần lễ là phần hội, phần này bao gồm những hoạt động vui chơi và ăn uống. ",
            "Ý nghĩa lễ hội":"Lễ hội Nghinh Ông mang đậm bản sắc văn hóa của người dân miền biển, được tổ chức mỗi năm 1 lần với mong ước: mưa thuận, gió hòa, làm ăn phát đạt. Đây cũng là dịp để ngư dân tỏ lòng biết ơn của mình và là dịp để vui chơi giải trí sau một năm làm lụng vất vả. Nếu bạn có dịp đến thì đừng bỏ lỡ lễ hội này nhé!"
        }
    },
    {
        "question": "Thông tin về lễ hội Thánh Gióng?",
        "options": ["Lễ hội Thánh Gióng là gì?", "Thời gian diễn ra?", "Địa điểm diễn ra?", "Nguồn gốc ý nghĩa?","Các hoạt động có trong lễ hội?"],
        "answers": {
            "Lễ hội Thánh Gióng là gì?":"Hội Gióng là một lễ hội truyền thống hàng năm ở nhiều nơi thuộc vùng Hà Nội để tưởng niệm và ca ngợi chiến công của người anh hùng truyền thuyết Thánh Gióng, một trong tứ bất tử của tín ngưỡng dân gian Việt Nam.<br>"
                                    +"Có 2 hội Gióng tiêu biểu ở Hà Nội là hội Gióng Sóc Sơn ở đền Sóc xã Phù Linh, huyện Sóc Sơn và hội Gióng Phù Đổng ở đền Phù Đổng, xã Phù Đổng, huyện Gia Lâm đã được UNESCO ghi danh là di sản văn hóa phi vật thể của nhân loại<br>"
                                    +"Ngoài ra còn hơn 10 hội Gióng cũng thuộc địa bàn Hà Nội (gọi là vùng lan tỏa vì chưa được UNESCO ghi danh) như: hội Gióng Bộ Đầu xã Thống Nhất, huyện Thường Tín; lễ hội thờ Thánh Gióng ở các làng Đổng Xuyên, Chi Nam (huyện Gia Lâm); các làng Phù Lỗ Đoài, Thanh Nhàn, Xuân Lai (huyện Sóc Sơn); Sơn Du, Cán Khê, Đống Đồ (huyện Đông Anh); Xuân Tảo (Phường Xuân Đỉnh, Quận Bắc Từ Liêm); làng Hội Xá (Quận Long Biên).", 
            "Thời gian diễn ra?":"Hội Gióng Phù Đổng chính thống được tổ chức hàng năm vào ba ngày mùng 7, mùng 8 và mùng 9 tháng 4 Âm lịch tại xã Phù Đổng, huyện Gia Lâm, thành phố Hà Nội, nơi sinh ra người anh hùng huyền thoại Phù Đổng Thiên Vương.", 
            "Địa điểm diễn ra?":"Lễ hội Gióng thường được tổ chức tại các đền thờ Thánh Gióng, trong đó nổi bật nhất là Đền Gióng ở Sóc Sơn, Hà Nội, nơi được xem là quê hương của Thánh Gióng.", 
            "Nguồn gốc ý nghĩa?":"Lễ hội Gióng không chỉ mang ý nghĩa tôn vinh Thánh Gióng mà còn thể hiện tinh thần yêu nước, đấu tranh chống giặc ngoại xâm của dân tộc. Lễ hội cũng là dịp để người dân cầu mong sự bình an, sức khỏe và thành công trong cuộc sống.",
            "Các hoạt động có trong lễ hội?":"Lễ dâng hương: Nghi lễ dâng hương được tiến hành tại đền, nơi người dân và du khách đến cầu nguyện và thể hiện lòng thành kính đối với Thánh Gióng.<br>"
                                            +"Rước kiệu: Một trong những hoạt động quan trọng là lễ rước kiệu, trong đó có sự tham gia của các thanh niên và người dân, mang theo kiệu của Thánh Gióng đi qua các con đường trong làng.<br>"
                                            +"Các hoạt động văn nghệ: Lễ hội cũng có nhiều tiết mục văn nghệ dân gian, như hát chầu văn, múa lân, biểu diễn các trò chơi truyền thống, tạo không khí vui tươi cho lễ hội.<br>"
                                            +"Thi đấu thể thao: Trong khuôn khổ lễ hội, còn có các trò chơi dân gian và thi đấu thể thao, thể hiện sức khỏe và sự khéo léo của người dân.<br>",
        }
    }
]

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
    
    
       
# Route để phục vụ trang web
@app.get("/")
def serve_homepage():
    return FileResponse('static/index.html')

# Model để nhận dữ liệu từ người dùng
class Answer(BaseModel):
    answer: str
    num: int
# # API để gửi câu hỏi tới giao diện người dùng
# @app.get("/get_question")
# async def get_question(num_class):
#     global current_question_index
    
#     current_question_index = int(num_class)
    
#     if current_question_index >= len(questions):
#         current_question_index = 0  # Reset nếu đã hết câu hỏi
#     question_data = questions[current_question_index]
#     return JSONResponse(content={
#         "question": question_data["question"],
#         "options": question_data["options"]
#     })

# # API để nhận câu trả lời và trả về phản hồi
# @app.post("/submit_answer")
# async def submit_answer(answer: Answer):
#     print("send answer ok")
#     print(answer.answer)
#     print(answer.num)
     
#     correct_response = questions[answer.num]["answers"].get(answer.answer, "Câu trả lời không hợp lệ.")
    
#     return JSONResponse(content={"response": correct_response})



# Chạy ứng dụng FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
    
#uvicorn app:app --reload