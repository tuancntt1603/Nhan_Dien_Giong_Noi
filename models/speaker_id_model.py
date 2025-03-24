import pickle
import numpy as np
import librosa

# Đường dẫn tới file mô hình
GMM_FILE = "trained_data/gmm_models.pkl"

# Tải mô hình GMM
with open(GMM_FILE, "rb") as f:
    gmm_models = pickle.load(f)

# Hàm trích xuất MFCC
def extract_mfcc(audio_path, sr=16000):
    audio, _ = librosa.load(audio_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return mfcc.T  # Shape: (frames, n_mfcc)

# Hàm tính RMS (năng lượng âm thanh)
def calculate_rms(audio_path, sr=16000):
    audio, _ = librosa.load(audio_path, sr=sr)
    rms = np.sqrt(np.mean(audio**2))
    return rms

def identify_speaker(audio_path, rms_threshold=0.01, score_threshold=-100):
    # Kiểm tra năng lượng âm thanh
    rms = calculate_rms(audio_path)
    if rms < rms_threshold:
        return "Không xác định (không có giọng nói)"

    # Trích xuất MFCC
    input_mfcc = extract_mfcc(audio_path)
    if input_mfcc is None or input_mfcc.size == 0:
        return "Không xác định (lỗi trích xuất MFCC)"

    # Tính điểm số cho từng người nói
    scores = {}
    for name, gmm in gmm_models.items():
        score = gmm.score(input_mfcc)
        scores[name] = score
        print(f"{name}: {score}")  # In điểm số để kiểm tra

    # Tìm người nói có điểm số cao nhất
    identified_speaker = max(scores, key=scores.get)
    max_score = scores[identified_speaker]

    # So sánh với ngưỡng
    if max_score < score_threshold:
        return "Không xác định (xác suất thấp)"
    else:
        print(f"Nhận diện: {identified_speaker} (Score: {max_score})")
        return identified_speaker