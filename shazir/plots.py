import matplotlib.pyplot as plt
import numpy as np
import librosa
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MaxNLocator

def plot_spectrogram(times, frequencies, amplitudes, dir_output, track_name = None):

    '''plot_spectrogram: plots the spectrogram

    Args:
        times: array containing the time samples
        frequencies: array containing the frequency samples
        amplitudes: array containing the spectrogram amplitudes
            amplitudes.shape = (frequencies.shape, times.shape)
    '''
    width = int(0.1 * times[-1])
    fig, ax = plt.subplots(figsize=(width,10))
    out = ax.pcolormesh(times, frequencies, amplitudes, cmap='Greys')
    _ = ax.set_xlim(times.min(), times.max())
    _ = ax.set_ylim(frequencies.min(), frequencies.max())
    thresh = librosa.note_to_hz("C2")  # Defines the range (-x, x), 
                                       # within which the plot is linear
    ax.set_yscale('symlog', base=2, linthresh=thresh)
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_label_text("Frequency [Hz]")
    ax.xaxis.set_label_text("Time [s]")

    if track_name is None:
        title = 'Spectrogram'
        export_name = dir_output + 'Spectrogram.jpg'
    else:
        title = f'Spectrogram of {track_name}'
        export_name = dir_output + f'Spectrogram_{track_name}.jpg'

    plt.title(title)  

    # fig.colorbar(out)
    cax = fig.add_axes([ax.get_position().x1 + 0.25 / width, ax.get_position().y0, 0.3 / width ,ax.get_position().height])
    fig.colorbar(out, cax=cax)

    plt.savefig(export_name, bbox_inches='tight')

    
def plot_peaks_constellation(frequencies, times, peaks_times, peaks_frequencies,
    dir_output, track_name = None):

    '''plot_peaks_constellation: plots the constallation map for the
    spectrogram peaks.

    Args:
        frequencies: array containing the frequency samples
        peaks_times: time values for the peaks
        peaks_frequencies: frequency values for the peaks
        track_name: name of the track (optional)
    '''

    width = int(0.1 * times[-1])
    fig, ax = plt.subplots(figsize=(width,10))
    out = ax.scatter(peaks_times, peaks_frequencies, marker='x', s=20)
    ax.set_ylim(frequencies.min(), frequencies.max())
    thresh = librosa.note_to_hz("C2")  # Defines the range (-x, x)
                                       # within which the plot is linear
    ax.set_yscale('symlog', base=2, linthresh=thresh)
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_label_text("Frequency [Hz]")
    ax.xaxis.set_label_text("Time [s]")

    if track_name is None:
        title = 'Constellation Map'
        export_name = dir_output + 'Constellation_map.jpg'
    else:
        title = f'Constellation Map of {track_name}'
        export_name = dir_output + f'Constellation_{track_name}.jpg'

    plt.title(title)
    plt.savefig(export_name, bbox_inches='tight')


def plot_matching_hash_locations(fingerprints_track, fing_rec,
    dir_output, track_name = None):

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

        ax.scatter(matching_times_track, matching_times__recording, s=100, 
            facecolors="None", edgecolor='red')  

        plt.xlabel('Track time [s]')
        plt.ylabel('Sample time [s]')
        plt.grid()

        if track_name is None:
            title = f'Scatterplot of matching hash locations (score: {score})'
            export_name = dir_output + 'Matching_hash_locations.jpg'
        else:
            title = f'Scatterplot of matching hash locations of {track_name} (score: {score})' 
            export_name = dir_output + f'Matching_hash_locations_{track_name}.jpg'

        plt.title(title)
        plt.savefig(export_name)
    
    def _plot_histogram_time_offsets_differences(time_offset_differences, score):

        fig, ax = plt.subplots(figsize=(20,10))
        plt.hist(time_offset_differences)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        if track_name is None:
            title = f'Histogram of differences of time offsets (score = {score})'
            export_name = dir_output + 'Histogram_time_offsets_differences.jpg'
        else:
            title = f'Histogram of differences of time offsets of {track_name} (score = {score})'
            export_name = dir_output + f'Histogram_time_offsets_differences_{track_name}.jpg'
        
        plt.xlabel('Offset track time - offset sample time [s]')
        plt.title(title)
        plt.savefig(export_name)

    matches = []

    [matches.append([fingerprints_track[k], fing_rec[k], fingerprints_track[k] -
        fing_rec[k]]) if k in fingerprints_track else None
        for k in fing_rec.keys()]   

    score = max(np.histogram([m[2] for m in matches], bins='auto')[0])

    _plot_hash_locations([m[0] for m in matches],[m[1] for m in matches], score)
    _plot_histogram_time_offsets_differences([m[2] for m in matches], score)
    
    return 