import numpy as np

def compute_track_score(fingerprints_track, fingerprints_recording,
    return_offset_differences = False):

    time_offset_differences = []

    [[time_offset_differences.append((h[0] - hS[0])) if hS[1:] == h[1:]
        else None for h in fingerprints_track] for hS in fingerprints_recording]
    
    if not return_offset_differences:
        return max(np.histogram(time_offset_differences, bins='auto')[0])
    else:
        return max(np.histogram(time_offset_differences, bins='auto')[0]), time_offset_differences


if __name__ == '__main__':

    from fingerprinting import make_fingerprint
    import time

    dir = '../resources/'
    track_file = 'Coldplay-VioletHill.wav'
    sample_file = 'Sample.wav'
    
    fingerprints_track = make_fingerprint(dir + track_file)
    fingerprints_sample = make_fingerprint(dir + sample_file)

    time_start = time.time()
    score = compute_track_score(fingerprints_track, fingerprints_sample)
    time_end = time.time()
    print(score)
    
    print(f'Running time: {time_end - time_start} s') 