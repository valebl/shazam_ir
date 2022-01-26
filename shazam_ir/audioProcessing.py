import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import IPython.display as ipd

from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import SymmetricalLogLocator
from scipy.signal import argrelextrema

# FRAME_SIZE = 2048
# HOP_SIZE = 512

def processAudioFile(audioFile, FRAME_SIZE, HOP_SIZE):

    '''
    This function takes a .wav audio file and returns the parameters
    defining its spectrogram, calculated using the library librosa.
    Arguments:
    - audioFile: audio track in .wav format
    - FRAME_SIZE: number of samples in the time frame - should be a power of two
    - HOP_SIZE: number of time samples in between successive frames - should be a power of two
    '''

    audioSignal, sampleRate = librosa.load(audioFile)
    audioStft = librosa.stft(audioSignal, n_fft=FRAME_SIZE, hop_length=HOP_SIZE) # Short-Time Fourier-Transform
    y_audio = np.abs(audioStft) ** 2
    y_log_audio = librosa.power_to_db(y_audio) # decibel
    times = librosa.frames_to_time(np.arange(y_log_audio.shape[1]), sr=sampleRate, hop_length=HOP_SIZE)
    frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=FRAME_SIZE)

    return times, frequencies, y_log_audio


def makePeaksConstellation(times, frequencies, amplitudes, ampThresh):

    '''
    This function identifies peaks in the spectrogram. Peaks are
    time-frequency points that have higher energy content then all
    their neighbours. An minimum amplitude threshold is also considered.
    Arguments:
    - times: array containing the time samples
    - frequencies: array containing the frequency samples
    - amplitudes = array containing the spectrogram amplitudes
      amplitudes.shape = (frequencies.shape, times.shape)    
    - ampThresh: minimum amplitude value for a point to be considered
      a candidate peak
    '''

    peaks = argrelextrema(amplitudes > ampThresh, np.greater)
    correspondentTime = lambda i: times[i]
    correspondentFreq = lambda i: frequencies[i]
    peaksFrequencies = correspondentFreq(peaks[0])
    peaksTimes = correspondentTime(peaks[1])

    return peaksTimes, peaksFrequencies


def plotSpectrogram(times, frequencies, amplitudes):

    '''
    This function plots the spectrogram.
    Arguments:
    - times: array containing the time samples
    - frequencies: array containing the frequency samples
    - amplitudes = array containing the spectrogram amplitudes
      amplitudes.shape = (frequencies.shape, times.shape)
    '''

    fig, ax = plt.subplots(figsize=(25,10))
    axes = plt.gca()
    out = axes.pcolormesh(times, frequencies, amplitudes, cmap='Greys')
    _ = axes.set_xlim(times.min(), times.max())
    _ = axes.set_ylim(frequencies.min(), frequencies.max())
    thresh = librosa.note_to_hz("C2") # Defines the range (-x, x), within which the plot is linear
    axes.set_yscale('symlog', base=2, linthresh=thresh)
    axes.yaxis.set_major_formatter(ScalarFormatter())
    axes.yaxis.set_label_text("Frequency [Hz]")
    axes.xaxis.set_label_text("Time [s]")
    fig.colorbar(out)
    plt.title('Spectrogram')
    plt.show()

    
def plotPeaksConstellation(frequencies, peaksTimes, peaksFrequencies):

    '''
    This function plots the constallation map for the spectrogram peaks.
    Arguments:
    - frequencies: array containing the frequency samples
    - peaksTimes: time values for the peaks
    - peaksFrequencies: frequency values for the peaks
    '''

    fig, ax = plt.subplots(figsize=(25,10))
    axes = plt.gca()
    out = axes.scatter(peaksTimes, peaksFrequencies, s=5)
    axes.set_ylim(frequencies.min(), frequencies.max())
    thresh = librosa.note_to_hz("C2") # Defines the range (-x, x), within which the plot is linear
    axes.set_yscale('symlog', base=2, linthresh=thresh)
    axes.yaxis.set_major_formatter(ScalarFormatter())
    axes.yaxis.set_label_text("Frequency [Hz]")
    axes.xaxis.set_label_text("Time [s]")
    plt.title('Constellation Map')
    plt.show()