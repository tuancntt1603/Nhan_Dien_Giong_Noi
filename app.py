from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
import os
import tempfile
from models.speaker_id_model import identify_speaker

app = Flask(__name__)
socketio = SocketIO(app)

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@socketio.on('audio_data')
def handle_audio_data(audio_blob):
    fd, tmp_file_path = tempfile.mkstemp(suffix=".wav")
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(audio_blob)
    speaker = identify_speaker(tmp_file_path)
    if speaker.startswith("Không xác định"):
        socketio.emit('speaker_result', {'speaker': None, 'message': speaker})
    else:
        socketio.emit('speaker_result', {'speaker': speaker})
    os.remove(tmp_file_path)

@socketio.on('add_to_history')
def add_to_history(data):
    conversation_history.append(data)

@socketio.on('save_history')
def save_history():
    filename = 'conversation_history.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in conversation_history:
            f.write(f"{entry['speaker']}: {entry['transcript']}\n")
    socketio.emit('download_history', {'file': filename})

if __name__ == '__main__':
    socketio.run(app, debug=True)