from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import io
import os
import tempfile
import wave
from pydub import AudioSegment
from speech_recognition import AudioData, Recognizer, UnknownValueError
from models.speaker_id_model import identify_speaker

app = Flask(__name__)
socketio = SocketIO(app)

# Biến trạng thái toàn cục
current_speaker = None  # Người nói hiện tại; nếu chưa có thì là None
transcript = []         # Lịch sử hội thoại

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("audio_data")
def handle_audio_data(audio_blob):
    global current_speaker, transcript
    try:
        print("Nhận được audio_blob, kích thước:", len(audio_blob))
        # Tạo file tạm để lưu blob (định dạng .webm)
        fd, tmp_file_path = tempfile.mkstemp(suffix=".webm")
        with os.fdopen(fd, 'wb') as tmp:
            tmp.write(audio_blob)
        file_size = os.path.getsize(tmp_file_path)
        print("Đã lưu file tạm:", tmp_file_path, "Kích thước:", file_size)
        
        # Nếu file tạm quá nhỏ, bỏ qua xử lý (có thể không chứa dữ liệu hợp lệ)
        if file_size < 1000:
            print("File tạm quá nhỏ (", file_size, " bytes), bỏ qua xử lý.")
            os.remove(tmp_file_path)
            return
        
        # Sử dụng pydub để chuyển đổi file WebM sang WAV (pydub sử dụng FFmpeg)
        try:
            audio_segment = AudioSegment.from_file(tmp_file_path, format="webm")
            wav_io = io.BytesIO()
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)
        except Exception as e:
            raise Exception(f"Lỗi chuyển đổi file bằng pydub: {repr(e)}")
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
        
        wav_bytes = wav_io.getvalue()
        print("Kích thước dữ liệu WAV:", len(wav_bytes))
        wav_io.seek(0)
        
        # Tạo đối tượng AudioData từ dữ liệu WAV
        try:
            sample_rate = audio_segment.frame_rate
            sample_width = audio_segment.sample_width  # Số byte mỗi sample
            audio_data = AudioData(wav_bytes, sample_rate=sample_rate, sample_width=sample_width)
        except Exception as e:
            raise Exception(f"Lỗi tạo AudioData: {repr(e)}")
        
        recognizer = Recognizer()
        try:
            text = recognizer.recognize_google(audio_data, language="vi-VN").lower()
            print("Recognized text:", text)
        except UnknownValueError:
            print("Không nhận dạng được giọng nói.")
            text = ""
        except Exception as rec_e:
            raise Exception(f"Lỗi khi nhận dạng giọng nói: {repr(rec_e)}")
        
        # Xử lý văn bản nhận được:
        if "kết thúc cuộc gọi" in text:
            # Lệnh kết thúc cuộc gọi: lưu transcript, nhưng không xóa lịch sử
            emit("transcript_update", {"keyword": "kết thúc cuộc gọi", "message": "Cuộc gọi đã kết thúc. Transcript đã được lưu."})
            save_transcript_to_file()
            current_speaker = None  # reset người nói (nhưng transcript vẫn giữ lịch sử)
        elif current_speaker is None and "bắt đầu" in text:
            # Nếu chưa có người nói, khi nhận từ khóa "bắt đầu" sẽ nhận diện người nói
            try:
                wav_io.seek(0)
                speaker = identify_speaker(wav_io)
            except Exception as id_e:
                speaker = "Không xác định"
                print(f"Lỗi khi nhận diện người nói: {repr(id_e)}")
            current_speaker = speaker
            message = f"Đã nhận diện được {speaker}, mời {speaker} nói."
            emit("transcript_update", {"keyword": "bắt đầu", "speaker": speaker, "message": message})
            transcript.append(message)
        elif "kết thúc" in text and current_speaker is not None:
            # Khi nói "kết thúc", kết thúc phiên của người nói hiện tại (lịch sử vẫn giữ)
            message = f"Kết thúc lời nói của {current_speaker}."
            emit("transcript_update", {"keyword": "kết thúc", "speaker": current_speaker, "message": message})
            transcript.append(message)
            current_speaker = None
        elif current_speaker is not None:
            # Nếu có người nói đã được nhận diện, ghi lại nội dung của người đó
            content = f"{current_speaker}: {text}"
            transcript.append(content)
            emit("transcript_update", {"keyword": None, "speaker": current_speaker, "message": content})
        else:
            # Nếu không có người nói được nhận diện, ghi nhận nội dung chung
            transcript.append(text)
            emit("transcript_update", {"keyword": None, "speaker": None, "message": text})
                
    except Exception as e:
        error_message = f"[Lỗi: {repr(e)}]"
        print("Lỗi xử lý âm thanh:", error_message)
        emit("transcript_update", {"keyword": None, "speaker": None, "message": error_message})
        
def save_transcript_to_file():
    try:
        with open("transcript.txt", "w", encoding="utf-8") as f:
            for line in transcript:
                f.write(line + "\n")
        print("Transcript saved to transcript.txt")
    except Exception as e:
        print(f"Lỗi khi lưu transcript: {repr(e)}")
    
@app.route("/save", methods=["POST"])
def save_transcript():
    save_transcript_to_file()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    socketio.run(app, debug=True)
