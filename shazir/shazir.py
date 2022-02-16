import json
import sys
import pandas as pd

from recorder import Recorder
from fingerprints import fingerprint_recording
from search import searching_matching_track

if __name__ == '__main__':

    AMP_THRES = 0.7
    record = False

    with open("../resources/database/fingerprints_dict.json") as file:
        fingerprints_db = json.load(file)
    
    metadata_db = pd.read_csv('../resources/database/metadata_db.csv')

    if len(sys.argv) == 2 and str(sys.argv[1]).endswith('.wav'):
        recording_file = str(sys.argv[1])
        recording_file = 'recording.wav'
        fingerprints_recording = fingerprint_recording(recording_file,
            amp_thresh=AMP_THRES)
        searching_matching_track(fingerprints_db, metadata_db, fingerprints_recording)
    else:
        record = True
    
    while record:
        recorder = Recorder()
        recorder.record()
        try:
            fingerprints_recording = fingerprint_recording(recorder.recording,
                amp_thresh=AMP_THRES)
            searching_matching_track(fingerprints_db, metadata_db, fingerprints_recording)
        except:
            record = False
        
        

    