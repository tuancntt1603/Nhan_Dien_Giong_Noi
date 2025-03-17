import json
import numpy as np
import librosa

# Đường dẫn đến file JSON chứa MFCC mẫu cho từng người
MFCC_FILE = "trained_data/speaker_mfcc.json"

with open(MFCC_FILE, "r", encoding="utf-8") as f:
    speaker_mfcc = json.load(f)

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return -1
    return dot / (norm1 * norm2)

def extract_mfcc(audio_path, sr=16000):
    audio, _ = librosa.load(audio_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)

def identify_speaker(audio_path):
    """
    Nhận diện người nói từ file âm thanh đầu vào.
    So sánh MFCC của file đầu vào với dữ liệu mẫu trong speaker_mfcc.json.
    Trả về tên người nói nếu độ tương đồng vượt qua ngưỡng (0.65), ngược lại trả về "Không xác định".
    """
    input_mfcc = extract_mfcc(audio_path)
    best_similarity = -1
    identified_speaker = "Không xác định"
    threshold = 0.65  # Giá trị ngưỡng có thể điều chỉnh
    print(f"MFCC từ âm thanh đầu vào: {input_mfcc.tolist()}")
    for name, ref_mfcc in speaker_mfcc.items():
        ref_vec = np.array(ref_mfcc)
        sim = cosine_similarity(input_mfcc, ref_vec)
        print(f"Similarity với {name}: {sim}")
        if sim > best_similarity and sim > threshold:
            best_similarity = sim
            identified_speaker = name
    print(f"Nhận diện: {identified_speaker} (Similarity: {best_similarity})")
    return identified_speaker
