# Audio Extraction, Noise Cancellation, and Visualization with Python

This project demonstrates how to extract audio from video files, perform noise cancellation on audio files, and display video and audio waveforms side by side using various Python libraries including `librosa`, `noisereduce`, `soundfile`, `matplotlib`, `numpy`, `subprocess`, `pathlib`, `cv2`, and `os`.

## Requirements

Install the necessary libraries using pip:

'''bash
pip install librosa noisereduce soundfile matplotlib numpy opencv-python
'''
You also need to have ffmpeg installed. You can download it from here.

You also need to have ffmpeg installed. You can download it from here.

Functions
audioFileCheck
This function checks for audio files with specific extensions (.mp3, .wav) in a given directory.

extract_audio_from_mp4
This function extracts audio from an MP4 video file and saves it as a WAV file using ffmpeg.

noise
This function performs noise cancellation on an audio file using librosa and noisereduce, and saves the cleaned audio file.

noise_cancellation
This function processes a directory or a single file. It extracts audio from MP4 files if necessary, and applies noise cancellation to the audio files.

display_video_and_waveform
This function displays a video and its corresponding audio waveform side by side using cv2 for video and librosa for audio.
