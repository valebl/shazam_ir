from helpers import process_audio_file, make_peaks_constellation, make_combinatorial_hashes

def make_fingerprint(audio_file, frame_size = 2048, hop_size = 512,
    amp_thresh = 35, offset_time = 1, offset_freq = 10, delta_time = 10,
    delta_freq = 100, fan_out = 10):

    '''make_fingerprint

    Args:
        audio_file: 
        frame_size: 
        hop_size:
        amp_thresh: 
        offset_time:
        offset_freq:
        delta_time:
        delta_freq:
        fan_out:

    Returns:

    '''
    
    times, frequencies, amplitudes = process_audio_file(audio_file,
        frame_size, hop_size)

    peaks_times, peaks_frequencies = make_peaks_constellation(times,
        frequencies, amplitudes, amp_thresh)
    
    fingerprint_hashes = make_combinatorial_hashes(peaks_times,
        peaks_frequencies, offset_time, offset_freq, delta_time, delta_freq)
    
    return fingerprint_hashes


if __name__ == '__main__':

    import time

    dir = '../resources/'
    audio_file = 'Coldplay-VioletHill.wav'

    time_start = time.time()
    fingerprints = make_fingerprint(dir + audio_file)
    time_end = time.time()

    print(f'Running time: {time_end - time_start} s') 