import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import IPython.display as ipd

# FRAME_SIZE = 2048
# HOP_SIZE = 512

def processAudioFile(audioFile, FRAME_SIZE, HOP_SIZE):

    '''
    This function takes a .wav audio file and returns the parameters
    defining its spectrogram, calculated using the library librosa.
    Parameters:
    - audioFile: audio track in .wav format
    - FRAME_SIZE: number of samples in the time frame - should be a power of two
    - HOP_SIZE: number of time samples in between successive frames - should be a power of two
    '''

    audioSignal, sampleRate = librosa.load(audioFile)
    audioStft = librosa.stft(audioSignal, n_fft=FRAME_SIZE, hop_length=HOP_SIZE) # Short-Time Fourier-Transform
    y_audio = np.abs(audioStft) ** 2
    y_log_audio = librosa.power_to_db(y_audio) # decibel
    time = librosa.frames_to_time(np.arange(y_log_audio.shape[1]), sr=sampleRate, hop_length=HOP_SIZE)
    frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=FRAME_SIZE)

    return time, frequencies, y_log_audio