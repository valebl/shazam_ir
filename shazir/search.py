import numpy as np

MINIMUM_SCORE = 20

def searching_matching_track(fingerprints_dict, metadata_db, fingerprints_recording):

    '''searching_matching_track: finds all matching hashes between the 
    recording and the tracks in the database and computes the score for
    each track, thus identifying if there is a match.
    
    Args:
        hash_database: 
        metadata_db: 
        fingerprints_recording:
    '''
    
    time_offset_dict = dict()
    match = None
    max_score = 0

    for k in fingerprints_recording.keys():
        if k in fingerprints_dict.keys():
            for track_id in fingerprints_dict[k].keys():
                try:
                    time_offset_dict[track_id].append(fingerprints_dict[k][track_id] - fingerprints_recording[k])
                except:
                    time_offset_dict[track_id] = [fingerprints_dict[k][track_id] - fingerprints_recording[k]]
                    
    for track_id in time_offset_dict.keys():         
        track_score = max(np.histogram(time_offset_dict[track_id], bins='sqrt')[0])
        if track_score > max_score:
            match = track_id
            max_score = track_score
    
    if max_score < MINIMUM_SCORE:
        print('Scores are too low :( Try again, perhaps with a longer recording!')
    else:
        title = metadata_db.loc[int(match)]['title']
        print(f'The best match is {title} (score = {max_score})')
    
    