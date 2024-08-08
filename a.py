import sys
import librosa
import noisereduce as nr
import soundfile as sf
import numpy as np
import subprocess
from pathlib import Path
import cv2
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

extentions = ['.mp3', '.wav']

def audioFileCheck(path):
    dirlist = []
    for i in os.listdir(path):
        _, extention = os.path.splitext(i)
        if extention in extentions:
            dirlist.append(i)
    return dirlist

def extract_audio_from_mp4(file, output_dir):
    base = Path(file).stem
    audio_file = Path(output_dir) / f'{base}.wav'
    command = f'ffmpeg -i "{file}" -q:a 0 -map a "{audio_file}" -y'
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error extracting audio: {result.stderr}")
    else:
        print(f"Extracted audio to: {audio_file}")
    return str(audio_file)

def noise(file, path_des):
    y, sr = librosa.load(file, sr=None)
    reduce_noise = nr.reduce_noise(y=y, sr=sr)
    outputfile = Path(path_des) / f'{Path(file).stem}_cleaned.wav'
    print(f"Saving cleaned file to: {outputfile}")
    sf.write(outputfile, reduce_noise, sr)

def noise_cancellation(path_sr, path_des):
    os.makedirs(path_des, exist_ok=True)
    if os.path.isfile(path_sr):
        if path_sr.endswith('.mp4'):
            path_sr = extract_audio_from_mp4(path_sr, path_des)
            if not os.path.exists(path_sr):
                print(f"Extracted file {path_sr} not found.")
                return 1
        noise(path_sr, path_des)
    elif os.path.isdir(path_sr):
        for i in audioFileCheck(path_sr):
            path = os.path.join(path_sr, i)
            if os.path.isfile(path):
                if path.endswith('.mp4'):
                    path = extract_audio_from_mp4(path, path_des)
                    if not os.path.exists(path):
                        print(f"Extracted file {path} not found.")
                        continue
                noise(path, path_des)
    else:
        return 1
    return 0

class VideoPlayer(QWidget):
    def __init__(self, video_path, audio_path):
        super().__init__()
        self.video_path = video_path
        self.audio_path = audio_path
        self.initUI()
        
        self.cap = cv2.VideoCapture(self.video_path)
        self.y, self.sr = librosa.load(self.audio_path, sr=None)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
        self.start_time = datetime.now()
        self.timer.start(30)
        
    def initUI(self):
        self.setWindowTitle('Video and Audio Waveform Player')
        
        # Video label
        self.video_label = QLabel(self)
        
        # Matplotlib figure and canvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([], [], color='r')
        
        # Set up layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.video_label)
        hbox.addWidget(self.canvas)
        
        self.setLayout(hbox)
        
        self.show()
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            return
        
        current_time = (datetime.now() - self.start_time).total_seconds()
        
        # Update video frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        
        # Update waveform
        self.ax.clear()
        librosa.display.waveshow(self.y, sr=self.sr, ax=self.ax, alpha=0.6)
        self.line, = self.ax.plot([current_time, current_time], [-1, 1], color='r')
        self.ax.set_xlim(0, self.duration)
        self.ax.set_ylim(-1, 1)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    source_path = 'C:/Users/lenovo/Desktop/sanya_proj/my.mp4'
    destination_path = 'C:/Users/lenovo/Desktop/sanya_proj/cleaned_audio'
    
    # Perform noise cancellation
    noise_cancellation(source_path, destination_path)
    
    # Assuming the cleaned audio is saved as my_cleaned.wav in the destination path
    cleaned_audio_path = os.path.join(destination_path, 'my_cleaned.wav')
    
    player = VideoPlayer(source_path, cleaned_audio_path)
    sys.exit(app.exec_())
