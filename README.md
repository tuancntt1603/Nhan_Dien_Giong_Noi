
# Hệ thống Nhận diện Giọng nói và Xác định Người nói

<div align="center">

<p align="center">
  <img src="https://github.com/drkhanusa/DNU_PlagiarismChecker/raw/main/docs/images/logo.png" alt="Logo" width="200"/>
  <img src="https://github.com/drkhanusa/DNU_PlagiarismChecker/raw/main/docs/images/AIoTLab_logo.png" alt="AIoTLab Logo" width="170"/>
</p>

[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SocketIO](https://img.shields.io/badge/SocketIO-010101?style=for-the-badge&logo=socket.io)](https://socket.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

</div>

<h3 align="center">Nhận diện Người nói và Ghi lại Lịch sử Cuộc họp theo Thời gian thực</h3>

<p align="center">
  <strong>Hệ thống sử dụng Flask, SocketIO, và mô hình GMM kết hợp MFCC để nhận diện người nói trong các phiên họp theo thời gian thực, đồng thời ghi lại lịch sử cuộc họp.</strong>
</p>

<p align="center">
  <a href="#-kiến-trúc-hệ-thống">Kiến trúc</a> •
  <a href="#-tính-năng-chính">Tính năng</a> •
  <a href="#-công-nghệ-sử-dụng">Công nghệ sử dụng</a> •
  <a href="#-cài-đặt">Cài đặt</a> •
  <a href="#-hướng-dẫn-sử-dụng">Hướng dẫn sử dụng</a> •
  <a href="#-đóng-góp">Đóng góp</a>
</p>

---

## 🏗️ Kiến trúc hệ thống

Hệ thống được xây dựng dựa trên kiến trúc ba tầng:

1. **Backend (Flask & SocketIO)**  
   - Nhận dữ liệu âm thanh từ client qua WebSocket.
   - Sử dụng mô hình GMM để nhận diện người nói dựa trên đặc trưng MFCC.
   - Quản lý và lưu trữ lịch sử cuộc họp vào file văn bản.

2. **Frontend (HTML, JavaScript)**  
   - Giao diện hiển thị trạng thái cuộc họp, thông tin người nói, và lịch sử hội thoại.
   - Sử dụng Web Speech API để ghi âm và chuyển giọng nói thành văn bản theo thời gian thực.
   - Giao tiếp với server qua SocketIO để cập nhật thông tin người nói và lịch sử hội thoại.

3. **Mô hình Nhận diện Người nói**  
   - Trích xuất đặc trưng MFCC từ các file âm thanh huấn luyện bằng _librosa_.
   - Huấn luyện mô hình Gaussian Mixture Model (GMM) cho từng người nói.
   - Dự đoán người nói bằng cách so sánh dữ liệu âm thanh đầu vào với các mô hình đã huấn luyện.

---

## 📂 Cấu trúc dự án
📦 Project<br>
├── 📂 audio                  # Thư mục chứa dữ liệu âm thanh<br>
│   ├── 📂 test              # Dữ liệu âm thanh để kiểm thử<br>
│   │   ├── 📂 anh_duong<br>
│   │   ├── 📂 anh_tuan<br>
│   │   ├── 📂 anh_uan<br>
│   ├── 📂 train             # Dữ liệu âm thanh để huấn luyện<br>
│   │   ├── 📂 anh_duong<br>
│   │   ├── 📂 anh_tuan<br>
│   │   ├── 📂 anh_uan<br>
├── 📂 images                # Thư mục chứa hình ảnh (logo, poster, v.v.)<br>
├── 📂 models                # Thư mục chứa mã nguồn mô hình nhận diện<br>
│   ├── 📂 pycache      # Cache của Python<br>
│   ├── speaker_id_model.py # Mô hình nhận diện người nói<br>
├── 📂 templates             # Thư mục chứa giao diện HTML<br>
│   ├── index.html          # Trang web chính<br>
├── 📂 trained_data          # Thư mục chứa dữ liệu đã huấn luyện<br>
│   ├── gmm_models.pkl      # File chứa mô hình GMM đã huấn luyện<br>
├── app.py                   # Ứng dụng Flask chính<br>
├── evaluate.py              # Script đánh giá độ chính xác của mô hình<br>
├── train.py                 # Script huấn luyện mô hình GMM<br>
├── README.md                # Tài liệu mô tả dự án<br>


---

## ✨ Tính năng chính

### 🎤 Nhận diện Người nói
- **Trích xuất MFCC:** Sử dụng _librosa_ để trích xuất đặc trưng MFCC từ file âm thanh với tần số lấy mẫu 16kHz và 13 hệ số MFCC.
- **Mô hình GMM:** Huấn luyện mô hình Gaussian Mixture Model với 16 thành phần cho từng người nói.
- **Dự đoán Người nói:** So sánh đặc trưng MFCC của âm thanh đầu vào với các mô hình GMM đã huấn luyện để xác định người nói.

### 📝 Ghi lại Lịch sử Cuộc họp
- **Chuyển Giọng Nói Thành Văn Bản:** Sử dụng Web Speech API để chuyển đổi giọng nói thành văn bản theo thời gian thực trên trình duyệt.
- **Lưu Lịch Sử:** Ghi lại thông tin người nói và nội dung hội thoại vào file `conversation_history.txt` khi cuộc họp kết thúc.

### 📡 Giao tiếp Thời gian thực
- **SocketIO:** Giao tiếp hai chiều giữa client và server để cập nhật thông tin người nói và lịch sử hội thoại mỗi giây.
- **Giao diện Người dùng:** Hiển thị trạng thái cuộc họp, thông tin người nói hiện tại, và lịch sử hội thoại trên trình duyệt với hiệu ứng động.

---

## 🔧 Công nghệ sử dụng

<div align="center">

### Core Technologies
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SocketIO](https://img.shields.io/badge/SocketIO-010101?style=for-the-badge&logo=socket.io)](https://socket.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

### Libraries & Tools
[![Librosa](https://img.shields.io/badge/Librosa-4C4C4C?style=for-the-badge)](https://librosa.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

</div>

---

## 📥 Cài đặt

### 🛠️ Yêu cầu trước
- **Python 3.8+**: Ngôn ngữ lập trình chính.
- **Microphone**: Thiết bị ghi âm để thu thập dữ liệu âm thanh từ giao diện web.
- **Các thư viện Python**: Flask, Flask-SocketIO, librosa, numpy, scikit-learn.

### 📦 Cài đặt các thư viện
1. Cài đặt Python từ [python.org](https://www.python.org/downloads/).
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install flask flask-socketio librosa numpy scikit-learn
### 📦 Chuẩn bị dữ liệu
- **Đặt các file âm thanh huấn luyện (.wav) vào thư mục audio/train/<tên_người_nói>/ (ví dụ: audio/train/anh_tuan/).**
- **Đặt các file âm thanh kiểm thử (.wav) vào thư mục audio/test/<tên_người_nói>/ (ví dụ: audio/test/anh_uan/)**<br>

### 🖥️ Hướng dẫn sử dụng
1. **Chuẩn bị dữ liệu:**<br>
- Đảm bảo các thư mục audio/train/ và audio/test/ chứa các file .wav của từng người nói (ví dụ: anh_dung, anh_tuan, anh_uan).<br>
- Mỗi thư mục con đại diện cho một người nói.
2. **Huấn luyện mô hình:**
- Chạy lệnh sau để huấn luyện mô hình GMM:
  ```bash
   python train.py
- Script sẽ trích xuất đặc trưng MFCC từ các file âm thanh trong audio/train/ và huấn luyện mô hình GMM cho từng người nói.
- Kết quả được lưu vào trained_data/gmm_models.pkl.
3. **Đánh giá mô hình:**
- Chạy lệnh sau để đánh giá độ chính xác của mô hình trên tập dữ liệu kiểm thử:
  ```bash
   python evaluate.py
- Script sẽ dự đoán người nói cho từng file trong audio/test/ và tính toán độ chính xác.
4. **Chạy ứng dụng chính:**
- Chạy lệnh sau để khởi động server Flask:
  ```bash
   python app.py
- Mở trình duyệt và truy cập http://localhost:5000 để sử dụng giao diện web.
5. **Sử dụng giao diện web:**
- Nhấn nút "Bắt đầu cuộc họp" để bắt đầu ghi âm và nhận diện người nói.
- Hệ thống sẽ:
- Ghi âm mỗi giây và gửi dữ liệu đến server để nhận diện người nói.
- Chuyển giọng nói thành văn bản và hiển thị trên giao diện.
- Khi một người nói xong (nói "kết thúc" hoặc "kết thúc cuộc họp"), hệ thống sẽ mời người tiếp theo phát biểu.
- Nhấn "Kết thúc cuộc họp" hoặc nói "kết thúc cuộc họp" để dừng ghi âm và tải file conversation_history.txt chứa lịch sử hội thoại.
<p align="center"> <img src="images/poster10.png" alt="System Architecture" width="800"/> </p>

## 🤝 Đóng góp
Dự án được phát triển bởi 4 thành viên:

| Họ và Tên       | Vai trò                  |
|-----------------|--------------------------|
| Nguyễn Công Uẩn | Phát triển mã nguồn, kiểm thử, triển khai dự án, thực hiện video giới thiệu và  làm Poster, Powerpoint.|
| Lê Xuân Dương | Hỗ trợ bài tập lớn, đề xuất cải tiến.|
| Đỗ Huy Dũng    | Thuyết trình, biên soạn Overleaf, hỗ trợ phát triển mã nguồn, hỗ trợ bài tập lớn.  |
| Bùi Anh Tuấn     | Hỗ trợ bài tập lớn, thu thập dữ liệu.      |

© 2025 NHÓM 10, CNTT16-03, TRƯỜNG ĐẠI HỌC ĐẠI NAM
