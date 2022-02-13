from skimage.feature import peak_local_max
from helpers import process_audio_file

def make_fingerprint(audio_file, frame_size = 2048, hop_size = 512,
    amp_thresh = 0.8, offset_time = 1, offset_freq = 500, delta_time = 10,
    delta_freq = 1000, fan_out = 10):

    '''make_fingerprint: takes in imput an audio file in .wav and performs
    the fingerprinting on it

    Args:
        audio_file: audio file in .wav
        frame_size: number of samples in the time frame - should be a
            power of two
        hop_size: number of time samples in between successive frames - should
            be a power of two
        amp_thresh: minimum amplitude value for a point to be considered
            a candidate peak
        offset_time: minimum time distance from the anchor point time value
            for a peak to be a possible pair 
        offset_frequency: minimum frequency distance from the anchor point
            frequency value for a peak to be a possible pair 
        delta_time: determines the maximum time value for a peak to be a
            possible pair
        delta_freq: determines the maximum frequency value for a peak to be
            a possible pair
        fan_out: maximum number of pairs for each peak in the combinatorial
            hashing

    Returns:
        A dictionary representing the fingerprints database
    '''
    
    times, frequencies, amplitudes = process_audio_file(audio_file,
        frame_size, hop_size)

    peaks_times, peaks_frequencies = make_peaks_constellation(times,
        frequencies, amplitudes, amp_thresh)
    
    fingerprints_dict = make_combinatorial_hashes(peaks_times,
        peaks_frequencies, offset_time, offset_freq, delta_time, delta_freq,
        fan_out)
    
    return fingerprints_dict


def fingerprint_track_and_add_to_database(track_file, track_id,
    fingerprints_db):

    '''fingerprint_track_and_add_to_database: takes a track, processes
    it and adds the fingerprints to the database, which is a dictionary
    where hashes are the keys and the value is another dictionary where
    the track_id is the key and the time offset is the value

    Args:
        track_file: 
        track_id: 
        fingerprints_db: 
    '''

    fingerprints_dict = make_fingerprint(track_file)

    for h in fingerprints_dict.keys():
        try:
            fingerprints_db[h][track_id] = fingerprints_dict[h]
        except:
            fingerprints_db[h] = {track_id: fingerprints_dict[h]}


def fingerprint_recording(recording_file, amp_thresh=35):

    fingerprints_dict = make_fingerprint(recording_file,
        amp_thresh=amp_thresh)

    return fingerprints_dict


### Helper functions in the following

def make_peaks_constellation(times, frequencies, amplitudes, amp_thresh):

    '''make_peaks_constellation: identifies peaks in the spectrogram. Peaks are
    time-frequency points that have higher energy content then all
    their neighbours. A minimum amplitude threshold is also considered.

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

    # start = time.time()
    peaks = peak_local_max(amplitudes, threshold_abs=amp_thresh)
    peaks_splitted = np.hsplit(peaks, 2)
    i = peaks_splitted[0]
    j = peaks_splitted[1]
    peaks_frequencies = frequencies[i]
    peaks_times = times[j]
    # end = time.time()
    # print(f'make_peaks_constellation took {end - start} s')

    return peaks_times, peaks_frequencies


def make_combinatorial_hashes(peaks_times, peaks_frequencies,
    offset_time, offset_freq, delta_time, delta_freq, fan_out):

    '''make_combinatorial_hashes: processes the spectogram peaks of a
    single track into its combinatorial hashes.

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

    # start = time.time()
    fan_out = 10
    for anchor_time, anchor_freq in zip(peaks_times, peaks_frequencies):
        _pairs_from_anchor_point(anchor_time, anchor_freq)
    # end = time.time()
    # print(f'make_combinatorial_hashes took {end - start} s') 

    return fingerprints_dict       



# if __name__ == '__main__':

#     import time

#     dir = '../resources/database/wav/'
#     audio_file = 'Milky-Chance_Stolen-Dance.wav'
#     recording_file = 'recording.wav'

#     time_start = time.time()
#     fingerprints = make_fingerprint(dir + audio_file)
#     time_end = time.time()

#     print(f'Fingerprinting track took {time_end - time_start} s') 

#     time_start = time.time()
#     fingerprints_recording = make_fingerprint(recording_file)
#     time_end = time.time()

#     print(f'Fingerprinting recording took {time_end - time_start} s') 

#     plot_matching_hash_locations(fingerprints, fingerprints_recording)