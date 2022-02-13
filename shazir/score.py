import numpy as np
from plots import plot_matching_hash_locations, plot_histogram_time_offsets_differences

def compute_track_score(fingerprints_track, fingerprints_recording):

    time_offset_diff = []

    [time_offset_diff.append((fingerprints_track[k] -
        fingerprints_recording[k])) if k in fingerprints_track else None
        for k in fingerprints_recording.keys()]   
    
    return max(np.histogram(time_offset_diff, bins='auto')[0])

def compute_track_score_with_plots(fingerprints_track, fingerprints_recording):

    matches = []

    [matches.append([fingerprints_track[k], fingerprints_recording[k], fingerprints_track[k] -
        fingerprints_recording[k]]) if k in fingerprints_track else None
        for k in fingerprints_recording.keys()]   

    plot_matching_hash_locations([m[0] for m in matches],[m[1] for m in matches])
    plot_histogram_time_offsets_differences([m[2] for m in matches])
    
    return max(np.histogram([m[2] for m in matches], bins='auto')[0])

# if __name__ == '__main__':

#     from fingerprints import make_fingerprint
#     import time

#     dir = '../resources/'
#     track_file = 'Coldplay-VioletHill.wav' # 'Elliott Smith-AFondFarewell.wav' # 
#     sample_file = 'Sample.wav'

#     start = time.time()  
#     fingerprints_track = make_fingerprint(dir + track_file)
#     end = time.time()
#     print(f'make_fingerprint on track took: {end - start} s') 

#     fingerprints_sample = make_fingerprint(dir + sample_file)

#     start = time.time()
#     score = compute_track_score_with_plots(fingerprints_track, fingerprints_sample)
#     end = time.time()
#     print(f'Score: {score}')
    
#     print(f'compute_track_score took: {end - start} s') 

#     print(len(fingerprints_sample))