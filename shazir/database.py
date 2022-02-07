import os
import pandas as pd
import json

from fingerprinting import fingerprint_track_and_add_to_database

def create_new_database():

    metadata_db = pd.DataFrame(columns=['track_id', 'title'])
    fingerprints_dict = dict()

    cwd = os.getcwd()
    os.chdir('../resources/database/wav')

    for track_file in os.listdir():

        track_id = len(metadata_db.index)
        metadata_db.loc[track_id] = [track_id, track_id]
        
        fingerprint_track_and_add_to_database(track_file, track_id,
            fingerprints_dict)
    
    os.chdir('..')
    json.dump(fingerprints_dict, open( "fingerprints_dict.json", 'w' ) )
    os.chdir(cwd)



if __name__ == '__main__':

    create_new_database()