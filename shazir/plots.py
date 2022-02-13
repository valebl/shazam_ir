import matplotlib.pyplot as plt
import numpy as np
import librosa
from matplotlib.ticker import ScalarFormatter

def plot_spectrogram(times, frequencies, amplitudes, track_name = None):

    '''plot_spectrogram: plots the spectrogram

    Args:
        times: array containing the time samples
        frequencies: array containing the frequency samples
        amplitudes: array containing the spectrogram amplitudes
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

    if track_name is None:
        title = 'Spectrogram'
        export_name = 'Spectrogram.jpg'
    else:
        f'Spectrogram of {track_name}'
        f'Spectrogram_{track_name}.jpg'

    plt.title(title)    
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

    if track_name is None:
        title = 'Constellation Map'
        export_name = 'Constellation_map.jpg'
    else:
        title = f'Constellation Map of {track_name}'
        f'Constellation_{track_name}.jpg'

    plt.title(title)
    plt.savefig(export_name)


def plot_matching_hash_locations(fingerprints_track, fing_rec,
    track_name = None):

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

    def _plot_hash_locations(matching_times_track, matching_times__recording, score):
    
        fig, ax = plt.subplots(figsize=(20,10))
        axes = plt.gca()

        axes.scatter(matching_times_track, matching_times__recording, s=100, 
            facecolors="None", edgecolor='red')  

        plt.xlabel('Track time [s]')
        plt.ylabel('Sample time [s]')
        plt.grid()

        if track_name is None:
            title = f'Scatterplot of matching hash locations (score: {score})'
            export_name = 'Matching_hash_locations.jpg'
        else:
            title = f'Scatterplot of matching hash locations of {track_name} (score: {score})' 
            export_name = f'Matching_hash_locations_{track_name}.jpg'

        plt.title(title)
        plt.savefig(export_name)
    
    def _plot_histogram_time_offsets_differences(time_offset_differences, score):

        fig, ax = plt.subplots(figsize=(20,10))
        plt.hist(time_offset_differences)

        if track_name is None:
            title = f'Histogram of differences of time offsets (score = {score})'
            export_name = 'Histogram_time_offsets_differences.jpg'
        else:
            title = f'Histogram of differences of time offsets of {track_name} (score = {score})'
            export_name = f'Histogram_time_offsets_differences_{track_name}.jpg'

    matches = []

    [matches.append([fingerprints_track[k], fing_rec[k], fingerprints_track[k] -
        fing_rec[k]]) if k in fingerprints_track else None
        for k in fing_rec.keys()]   

    score = max(np.histogram([m[2] for m in matches], bins='auto')[0])

    _plot_hash_locations([m[0] for m in matches],[m[1] for m in matches], score)
    _plot_histogram_time_offsets_differences([m[2] for m in matches], score)
    
    return 