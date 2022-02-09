import numpy as np

def searching_matching_track(hash_database, metadata_db, fingerprints_recording):
    
    time_offset_dict = dict()
    track_ids = set()
    match = None
    max_score = 0

    for k in fingerprints_recording.keys():
        if k in hash_database.keys():
            for track_id in hash_database[k].keys():
                track_ids.add(track_id)
                try:
                    time_offset_dict[track_id].append(hash_database[k][track_id] - fingerprints_recording[k])
                except:
                    time_offset_dict[track_id] = [hash_database[k][track_id] - fingerprints_recording[k]]
                    
    for track_id in track_ids:             
        track_score = max(np.histogram(time_offset_dict[track_id], bins='auto')[0])
        if track_score > max_score:
            match = track_id
            max_score = track_score
    
    if match is None:
        print('No match, sorry :(')
    else:
        title = metadata_db.loc[int(match)]['title']
        print(f'The song is {title} (score = {max_score})')
    
    