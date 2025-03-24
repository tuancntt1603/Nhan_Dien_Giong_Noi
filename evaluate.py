import os
from models.speaker_id_model import identify_speaker

# Đường dẫn
TEST_DIR = "audio/test"

# Danh sách người nói
speakers = {
    "Anh Uẩn": "anh_uan",
    "Anh Tuấn": "anh_tuan",
}

correct = 0
total = 0

# Đánh giá từng file trong tập test
for name, folder_name in speakers.items():
    folder_path = os.path.join(TEST_DIR, folder_name)
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            predicted_speaker = identify_speaker(file_path)
            if predicted_speaker == name:
                correct += 1
            total += 1
            print(f"File: {file_name}, Thực tế: {name}, Dự đoán: {predicted_speaker}")

# Tính độ chính xác
accuracy = correct / total if total > 0 else 0
print(f"Độ chính xác: {accuracy * 100:.2f}%")