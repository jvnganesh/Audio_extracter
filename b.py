import librosa
import noisereduce as nr
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import subprocess
from pathlib import Path
import cv2
import os
from datetime import datetime

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

def display_video_and_waveform(video_path, audio_path):
    cap = cv2.VideoCapture(video_path)
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # Create a figure for displaying video and waveform side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Setup video subplot
    ax1.axis('off')
    
    # Setup waveform subplot
    librosa.display.waveshow(y, sr=sr, ax=ax2, alpha=0.6)
    line, = ax2.plot([0, 0], [-1, 1], color='r')
    ax2.set_xlim(0, duration)
    ax2.set_ylim(-1, 1)
    
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = 1 / frame_rate
    
    start_time = datetime.now()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        current_time = (datetime.now() - start_time).total_seconds()
        ax1.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        line.set_xdata([current_time, current_time])
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if int(current_time * 10) % 10 == 0:  # Update waveform plot every 0.1 seconds
            fig.canvas.draw_idle()
            plt.pause(0.001)
        
    cap.release()
    cv2.destroyAllWindows()
    plt.close()

# Example usage
source_path = 'C:/Users/lenovo/Desktop/sanya_proj/my.mp4'
destination_path = 'C:/Users/lenovo/Desktop/sanya_proj/cleaned_audio'

# Perform noise cancellation
noise_cancellation(source_path, destination_path)

# Assuming the cleaned audio is saved as my_cleaned.wav in the destination path
cleaned_audio_path = os.path.join(destination_path, 'my_cleaned.wav')

# Display the video and corresponding audio waveform side by side
display_video_and_waveform(source_path, cleaned_audio_path)
