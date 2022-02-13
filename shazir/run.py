import json
import pandas as pd

from recorder import Recorder
from fingerprinting import fingerprint_recording
from searching import searching_matching_track

if __name__ == '__main__':

    AMP_THRES = 0.6

    with open("../resources/database/fingerprints_dict.json") as file:
        fingerprints_db = json.load(file)
    
    metadata_db = pd.read_csv('../resources/database/metadata_db.csv')

    recorder = Recorder()
    recorder.record()

    recording_file = 'recording.wav' # '../Sample.wav'  # '../resources/Sample.wav' # 

    fingerprints_recording = fingerprint_recording(recording_file,
        amp_thresh=AMP_THRES)

    searching_matching_track(fingerprints_db, metadata_db, fingerprints_recording)

    