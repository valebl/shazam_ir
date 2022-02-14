import os
import pandas as pd
import json
import time

from fingerprints import fingerprint_track_and_add_to_database

def create_new_database():

    '''
    create_new_database: creates a database from scratch by looping
    over the tracks, processing, fingerprinting and adding each of them;
    the database is implemented by a dictionary of dictionaries; additionally
    it creates a database of metadata for the tracks, implemented by a pandas
    dataframe
    '''

    metadata_db = pd.DataFrame(columns=['track_id', 'title'])
    fingerprints_dict = dict()

    cwd = os.getcwd()
    os.chdir('../resources/database/wav')

    for track_file in os.listdir():

        try:
            fingerprint_track_and_add_to_database(track_file, fingerprints_dict,
                metadata_db)        
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