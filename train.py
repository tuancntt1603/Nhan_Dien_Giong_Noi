import os
import pickle
import numpy as np
import librosa
from sklearn.mixture import GaussianMixture

# Đường dẫn
TRAIN_DIR = "audio/train"
OUTPUT_DIR = "trained_data"
GMM_FILE = os.path.join(OUTPUT_DIR, "gmm_models.pkl")

# Tạo thư mục nếu chưa có
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Hàm trích xuất MFCC
def extract_mfcc(file_path, n_mfcc=13):
    audio, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T  # Shape: (frames, n_mfcc)

# Danh sách người nói
speakers = {
    "Anh Uẩn": "anh_uan",
    "Anh Tuấn": "anh_tuan",
}

# Huấn luyện GMM cho từng người nói
gmm_models = {}
for name, folder_name in speakers.items():
    folder_path = os.path.join(TRAIN_DIR, folder_name)
    mfcc_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            mfcc = extract_mfcc(file_path)
            mfcc_list.append(mfcc)
    
    if mfcc_list:
        # Kết hợp tất cả frame MFCC
        all_mfcc = np.vstack(mfcc_list)
        # Huấn luyện GMM với 16 thành phần
        gmm = GaussianMixture(n_components=16, covariance_type='diag', max_iter=200)
        gmm.fit(all_mfcc)
        gmm_models[name] = gmm
        print(f"Đã huấn luyện GMM cho {name}")
    else:
        print(f"Không tìm thấy file âm thanh trong {folder_path}")

# Lưu mô hình
with open(GMM_FILE, "wb") as f:
    pickle.dump(gmm_models, f)
print(f"Mô hình GMM đã được lưu vào {GMM_FILE}")