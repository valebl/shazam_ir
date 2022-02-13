import time
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from matplotlib.ticker import ScalarFormatter
from skimage.feature import peak_local_max
import os


def convert_mp3_to_wav():

    '''convert_mp3_to_wav: simple function to convert all mp3 files
    into wav files (for Windows operating system)    
    '''

    print(os.getcwd())
    os.chdir('../resources/database/mp3')
    os.system('for %i in (*.mp3) do ffmpeg -i "%i" "%~ni.wav"')
    os.chdir('../../../shazir')
    

def process_audio_file(audio_file, frame_size, hop_size):

    '''process_audio_file: takes a .wav audio file and returns the
    parameters defining its spectrogram, calculated using the librosa library.

    Args:
        audio_file: audio track in .wav format
        frame_size: number of samples in the time frame - should be a
            power of two
        hop_size: number of time samples in between successive frames - should
            be a power of two
    
    Returns:
        A tuple consisting of an array of time samples [s], an array of the
        frequency samples [Hz] and a 2D array of the amplitude [dB].
    '''

    print(f'Processing track: {audio_file}')
    start = time.time()
    audio_signal, sample_rate = librosa.load(audio_file)
    audio_stft = librosa.stft(audio_signal, n_fft=frame_size,
        hop_length=hop_size)  # Short-Time Fourier-Transform
    y_audio = np.abs(audio_stft)**2
    y_log_audio = librosa.power_to_db(y_audio)  # Decibel
    y_log_audio_norm = y_log_audio / y_log_audio.max()
    times = librosa.frames_to_time(np.arange(y_log_audio.shape[1]),
        sr=sample_rate, hop_length=hop_size)
    frequencies = librosa.fft_frequencies(sr=sample_rate, n_fft=frame_size)
    end = time.time()
    # print(f'process_audio_file took {end - start} s')

    return times, frequencies, y_log_audio_norm


def make_peaks_constellation(times, frequencies, amplitudes, amp_thresh):

    '''make_peaks_constellation: identifies peaks in the spectrogram. Peaks are
    time-frequency points that have higher energy content then all
    their neighbours. An minimum amplitude threshold is also considered.

    Args:
        times: array containing the time samples
        frequencies: array containing the frequency samples
        amplitudes = array containing the spectrogram amplitudes
            amplitudes.shape = (frequencies.shape, times.shape)    
        amp_thresh: minimum amplitude value for a point to be considered
            a candidate peak

    Returns:
        A tuple consisting of two arrays, respectively of the time and
        frequency coordinates of the spectogram peaks.
    '''

    start = time.time()
    peaks = peak_local_max(amplitudes, threshold_abs=amp_thresh)
    peaks_splitted = np.hsplit(peaks, 2)
    i = peaks_splitted[0]
    j = peaks_splitted[1]
    peaks_frequencies = frequencies[i]
    peaks_times = times[j]
    end = time.time()
    # print(f'make_peaks_constellation took {end - start} s')

    return peaks_times, peaks_frequencies


def make_combinatorial_hashes(peaks_times, peaks_frequencies,
    offset_time, offset_freq, delta_time, delta_freq, fan_out):

    '''make_combinatorial_hashes: processes the spectogram peaks into
    the audio hashes.

    Args:
        peaks_times: time values for the peaks
        peaks_frequencies: frequency values for the peaks
        offset_time: minimum time distance from the anchor point time value
            for a peak to be a possible pair 
        offset_frequency: minimum frequency distance from the anchor point
            frequency value for a peak to be a possible pair 
        delta_time: determines the maximum time value for a peak to be a
            possible pair
        delta_freq: determines the maximum frequency value for a peak to be
            a possible pair
    
    Returns:
        Returns a dictionary where hashes are the keys and the value is
        another dictionary where the track_id is the key and the time offset
        is the value
    '''

    def _pairs_from_anchor_point(anchor_time, anchor_freq):

        start_time = anchor_time + offset_time
        start_freq = anchor_freq - offset_freq
        i = 0
        n_pairs = 0

        for t in peaks_times:
            f = peaks_frequencies[i]
            if (t > start_time and t < start_time + delta_time and            
                f > start_freq and f < start_freq + delta_freq):
                if n_pairs < fan_out:
                    fingerprints_dict[str(hash((anchor_freq[0], f[0], t[0] -
                        anchor_time[0])))] = anchor_time[0]
                    n_pairs += 1
                else:
                    break
            i += 1 

    fingerprints_dict = dict()

    start = time.time()
    fan_out = 10
    for anchor_time, anchor_freq in zip(peaks_times, peaks_frequencies):
        _pairs_from_anchor_point(anchor_time, anchor_freq)
    end = time.time()
    # print(f'make_combinatorial_hashes took {end - start} s') 

    return fingerprints_dict       


def plot_spectrogram(times, frequencies, amplitudes, track_name = None):

    '''plot_spectrogram: plots the spectrogram.

    Args:
        times: array containing the time samples
        frequencies: array containing the frequency samples
        amplitudes = array containing the spectrogram amplitudes
            amplitudes.shape = (frequencies.shape, times.shape)
    '''

    fig, ax = plt.subplots(figsize=(25,10))
    axes = plt.gca()
    out = axes.pcolormesh(times, frequencies, amplitudes, cmap='Greys')
    _ = axes.set_xlim(times.min(), times.max())
    _ = axes.set_ylim(frequencies.min(), frequencies.max())
    thresh = librosa.note_to_hz("C2")  # Defines the range (-x, x), 
                                       # within which the plot is linear
    axes.set_yscale('symlog', base=2, linthresh=thresh)
    axes.yaxis.set_major_formatter(ScalarFormatter())
    axes.yaxis.set_label_text("Frequency [Hz]")
    axes.xaxis.set_label_text("Time [s]")
    fig.colorbar(out)
    title = 'Spectrogram' if track_name is None \
        else f'Spectrogram of {track_name}'
    plt.title(title)
    export_name = 'Spectrogram.jpg' if track_name is None \
        else f'Spectrogram_{track_name}.jpg'
    plt.savefig(export_name)

    
def plot_peaks_constellation(frequencies, peaks_times, peaks_frequencies,
    track_name = None):

    '''plot_peaks_constellation: plots the constallation map for the
    spectrogram peaks.

    Args:
        frequencies: array containing the frequency samples
        peaks_times: time values for the peaks
        peaks_frequencies: frequency values for the peaks
        track_name: name of the track (optional)
    '''

    fig, ax = plt.subplots(figsize=(25,10))
    axes = plt.gca()
    out = axes.scatter(peaks_times, peaks_frequencies, marker='x', s=20)
    axes.set_ylim(frequencies.min(), frequencies.max())
    thresh = librosa.note_to_hz("C2")  # Defines the range (-x, x)
                                       # within which the plot is linear
    axes.set_yscale('symlog', base=2, linthresh=thresh)
    axes.yaxis.set_major_formatter(ScalarFormatter())
    axes.yaxis.set_label_text("Frequency [Hz]")
    axes.xaxis.set_label_text("Time [s]")
    title = 'Constellation Map' if track_name is None \
        else f'Constellation Map of {track_name}'
    plt.title(title)
    export_name = 'Constellation_map.jpg' if track_name is None \
        else f'Constellation_{track_name}.jpg'
    plt.savefig(export_name)


def plot_matching_hash_locations(fingerprints_track, fing_rec):

    '''plot_matching_hash_locations: creates a scatterplot of the peaks
    time offsets with respect to the beginning of the audio, considering
    the track and the recording; additionally it creates a histogram with
    the differences of time offsets between the track and the recording

    Args:
        fingerprints_track: dictionary containing the track fingerprints
        fingerprints_recording: dictionary containing the recording
            fingerprints

    Returns:
        The score for the track
    '''

    def _plot_hash_locations(matching_times_track, matching_times__recording):
    
        fig, ax = plt.subplots(figsize=(20,10))
        axes = plt.gca()

        axes.scatter(matching_times_track, matching_times__recording, s=100, 
            facecolors="None", edgecolor='red')  

        plt.title('Scatterplot of matching hash locations')
        plt.xlabel('Track time [s]')
        plt.ylabel('Sample time [s]')
        plt.grid()
        plt.savefig('Matching_hash_locations.jpg')
    
    def _plot_histogram_time_offsets_differences(time_offset_differences):

        fig, ax = plt.subplots(figsize=(20,10))
        plt.hist(time_offset_differences)
        plt.savefig('Histogram_time_offsets_differences.jpg')

    matches = []

    [matches.append([fingerprints_track[k], fing_rec[k], fingerprints_track[k] -
        fing_rec[k]]) if k in fingerprints_track else None
        for k in fing_rec.keys()]   

    _plot_hash_locations([m[0] for m in matches],[m[1] for m in matches])
    _plot_histogram_time_offsets_differences([m[2] for m in matches])
    
    return max(np.histogram([m[2] for m in matches], bins='auto')[0])



if __name__ == '__main__':

    dir = './'
    audio_file = 'recording.wav'
    # dir ='../resources/database/wav/'
    # audio_file = 'Milky-Chance_Stolen-Dance.wav' # 'Coldplay_Violet-Hill.wav'
    # audio_file = 'Foo-Fighters_Everlong.wav'
    FRAME_SIZE = 2048
    HOP_SIZE = 512
    AMP_THRES = 0.4

    times, frequencies, y_log_audio = process_audio_file(dir+audio_file,
        FRAME_SIZE, HOP_SIZE)
    print(f'file {audio_file} processed...')

    plot_spectrogram(times, frequencies, y_log_audio, audio_file)

    peaks_times, peaks_frequencies = make_peaks_constellation(times,
        frequencies, y_log_audio, AMP_THRES)
    print(f'peaks identified...')

    plot_peaks_constellation(frequencies, peaks_times, peaks_frequencies,
        audio_file)    