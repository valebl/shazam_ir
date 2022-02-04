import numpy as np

def compute_track_score(fingerprints_track, fingerprints_recording,
    return_offset_differences = False):

    time_offset_diff = []

    [time_offset_diff.append((fingerprints_track[k] -
        fingerprints_recording[k])) if k in fingerprints_track else None
        for k in fingerprints_recording.keys()]   
    
    if not return_offset_differences:
        return max(np.histogram(time_offset_diff, bins='auto')[0])
    else:
        return max(np.histogram(time_offset_diff, bins='auto')[0]), time_offset_diff


if __name__ == '__main__':

    from fingerprinting import make_fingerprint
    import time

    dir = '../resources/'
    track_file = 'Elliott Smith-AFondFarewell.wav' # 'Coldplay-VioletHill.wav'
    sample_file = 'Sample.wav'

    start = time.time()  
    fingerprints_track = make_fingerprint(dir + track_file)
    end = time.time()
    print(f'make_fingerprint on track took: {end - start} s') 

    fingerprints_sample = make_fingerprint(dir + sample_file)

    start = time.time()
    score = compute_track_score(fingerprints_track, fingerprints_sample)
    end = time.time()
    print(f'Score: {score}')
    
    print(f'compute_track_score took: {end - start} s') 