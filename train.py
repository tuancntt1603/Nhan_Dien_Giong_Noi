import os
import json
import librosa
import numpy as np

AUDIO_DIR = "audio"
OUTPUT_DIR = "trained_data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "speaker_mfcc.json")

speakers = {
    "Anh Dương": "anh_duong",
    "Anh Uẩn": "anh_uan",
    "Anh Tuấn": "anh_tuan",
    "Anh Dũng": "anh_dung"
}

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def extract_mfcc(file_path, n_mfcc=13):
    audio, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfcc, axis=1).tolist()

speaker_mfcc = {}
for name, folder_name in speakers.items():
    folder_path = os.path.join(AUDIO_DIR, folder_name)
    mfcc_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            mfcc = extract_mfcc(file_path)
            mfcc_list.append(mfcc)
            print(f"Đã trích xuất MFCC từ {file_path}: {mfcc}")
    
    if mfcc_list:
        mfcc_avg = np.mean(mfcc_list, axis=0).tolist()
        speaker_mfcc[name] = mfcc_avg
        print(f"MFCC trung bình cho {name}: {mfcc_avg}")
    else:
        print(f"Không tìm thấy file âm thanh trong {folder_path}")

with open(OUTPUT_FILE, "w") as f:
    json.dump(speaker_mfcc, f, indent=4)
print(f"Dữ liệu đã được lưu vào {OUTPUT_FILE}")