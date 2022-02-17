Shazir
============
*Valentina Blasone*

This repository contains a simple implementation of the Shazam algorithm from the original paper of 2003 ([Wang et al. 2003](https://www.researchgate.net/publication/220723446_An_Industrial_Strength_Audio_Search_Algorithm)). The project is part of the Information Retrieval course of DSSC @ University of Trieste, from this the name, shazir.

Instructions
------------

Clone the repo.

    git clone 
    cd shazir

Create an isolated environment with `conda` from the `environment.yml` file provided.

    conda env create -f environment.yml

Activate the environment.

    conda activate shazir

Since PyAudio is not supported directly in Anaconda for the recent python versions, you need to install it using pip and the correct wheel. For python 3.9 64 bit the file is already provided in the repository (`PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`), otherwise you need to look at [PyAudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and download the correct wheel. In the folder where your .whl file is type:

    pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl 
    
Finally you need to unzip the fingerprints database in order to have a file `shazir/resources/database/fingerprints_dict.json`.
   

Run Shazir
--------------------

Run the program by typing:
    
    python shazir.py

A dialog box will appear, allowing you to record the desired audio sample. When ready to record, click on "Start recording". To stop, click on "Stop recording". The program will return you the track with the highest scory among the ones in the database. If all tracks score less than a minimum score (by default set as 20), a message will be displayed, asking to try recording a longer audio sample.

Alternatively, you can run the program providing a sample file from the command line. The sample must be in .wav:

    python shazir.py ../resources/sample_trimmed.wav

N.B. The database consists on the fingerprints of 162 tracks. Songs not in this small database cannot be detected.


What's inside the repository
--------------------

```
shazir  
|
└───resources
│   │   sample_trimmmed.wav
|   |   sample_recorded.wav
|   |   matching_track.wav
|   |   non-matching_track.wav
│   │
│   └───database
│       │   fingerprints_dict.zip
│       │   metadata_db.csv
│   
└───shazir
|   │   database.py
|   │   fingerprints.py
|   |   plots.py
|   |   preprocess.py
|   |   recorder.py
|   |   search.py
|   |   shazir.py
|
└───examples
|   |   matching_vs_non-matching_plots.ipynb
    
```

The `resources/` folder contains two examples of audio samples, `sample_trimmed.wav` is an audio sample obtained by trimming a part of the song "Coldplay_Violet-Hill.wav",
while `sample_recorded.wav` is an audio sample obtained by recording with the laptop microphone a part of the song "Ed-Sheeran_Thinking-Out-Loud.wav", which was being played  from a mobile phone. Moreover, `matching_track.wav` is the complete song "Coldplay_Violet-Hill.wav" and `non-matching_track.wav` is the complete song "The-Beatles_Hey-Jude.wav". These songs are used in the examples, against the sample trimmed from "Coldplay_Violet-Hill.wav".

The `resources/database/` folder contains the fingerprints database as a zip folder. As specified in the instructions, you need to unzip the file to get the corresponding .json file. Moreover, the folder contains the related metadata database as a .csv file. These files have been obtained "offline" by a preprocessing step. The user can create its own tracks fingerprints and metadata databases by using the script `shazir/database.py`. The script will preprocess all the .wav songs contained in the folder `resources/database/wav/`.

The `shazir/` folder contains all the python scripts necessary for the program to work:

- `preprocess.py`: functionalities to preprocess audio files and to extract the values defining the spectrogram 
- `fingerprints.py`: functionalities to perform audio fingerprinting, through peaks identification and combinatorial hashing, but also to fingerprint and add a new track to a given database
- `recorder.py`: class to record a sample audio from the microphone
- `search`: functionalities to perform the search for a matching track in the database
- `plots.py`: functionalities to plot the spectrogram (given times, frequencies, amplitudes), the peaks constellation (given frequencies, times, peaks times, peaks frequencies) and the track-sample matching scatterplot and histogram (given track and sample fingerprints)
- `database.py`: runnable file, to build the tracks fingerprinting databases (see above)
- `shazir.py`: runnable file, to actually run the program (see above)

The `examples` folder contains a jupyter notebook, which shows plots for the different stages of the algorithm for a matching and non-matching track. In this examples we can see how the plots resamble the results in ([Wang et al. 2003](https://www.researchgate.net/publication/220723446_An_Industrial_Strength_Audio_Search_Algorithm)).

