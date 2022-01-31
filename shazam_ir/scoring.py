import numpy as np

def compute_track_score(fingerprints_track, fingerprints_recording,
    return_offset_differences = False):

    time_offset_differences = []

    for hS in fingerprints_recording:
        for h in fingerprints_track:
            if (hS[1:] == h[1:]):
                time_offset_differences.append((h[0]-hS[0]))
    
    if not return_offset_differences:
        return max(np.histogram(time_offset_differences, bins='auto')[0])
    else:
        return max(np.histogram(time_offset_differences, bins='auto')[0]), time_offset_differences


if __name__ == '__main__':

    from fingerprinting import make_fingerprint

    dir = '../resources/'
    track_file = 'Coldplay-VioletHill.wav'
    sample_file = 'Sample.wav'
    
    fingerprints_track = make_fingerprint(dir + track_file)
    fingerprints_sample = make_fingerprint(dir + sample_file)

    score = compute_track_score(fingerprints_track, fingerprints_sample)
    print(score)