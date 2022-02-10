import os
import pandas as pd
import json
import time

from fingerprinting import fingerprint_track_and_add_to_database

def create_new_database():

    metadata_db = pd.DataFrame(columns=['track_id', 'title'])
    fingerprints_dict = dict()

    cwd = os.getcwd()
    os.chdir('../resources/database/wav')

    for track_file in os.listdir():

        try:
            track_id = str(len(metadata_db.index))
            metadata_db.loc[track_id] = [track_id, track_file]
            
            fingerprint_track_and_add_to_database(track_file, track_id,
                fingerprints_dict)
        except:
            print(f'Skipping track: {track_file}')
            continue
    
    os.chdir('..')
    json.dump(fingerprints_dict, open( "fingerprints_dict.json", 'w' ) )
    metadata_db.to_csv('metadata_db.csv')
    os.chdir(cwd)



if __name__ == '__main__':

    start = time.time()
    create_new_database()
    end = time.time()
    print(f'Running time: {end - start}')