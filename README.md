Shazir
============
*Valentina Blasone*

This repository contains a simple implementation of the Shazam algorithm from the original paper of 2003 ([Wang et al. 2003](https://www.researchgate.net/publication/220723446_An_Industrial_Strength_Audio_Search_Algorithm)).

Instructions
------------

Clone the repo.

    $ git clone 
    $ cd shazir

Setup an isolated environment with `conda`.

    $ conda create -n shazir
    $ conda activate shazir

Installing Packages
--------------------

Get the requirements installed in the environment.

    $ conda install -c conda-forge --file requirements.txt
   

Run Shazir
--------------------

Run the program by typing:
    
    $ python shazir.py

A dialog box will appear, allowing you to record the desired audio sample. When ready to record, click on "Start recording". To stop, click on "Stop recording". The program will return you the track with the highest scory among the ones in the database. If all tracks score 0, a "no match" message will be displayed.

Alternatively, you can run the program providing a sample file from the command line. The sample must be in .wav:

    $ python shazir.py ../resources/Sample.wav

N.B. The database consists on the fingerprints of 163 tracks. Songs not in this small database has cannot be detected.


What's inside the repository
--------------------

```
shazir  
│
└───resources
│   │   Sample_trimmmed.wav
|   |   Sample_recorded.wav
│   │
│   └───database
│       │   fingerprints_dict.json
│       │   metadata_db.csv
│   
└───shazir
    │   database.py
    │   fingerprints.py
    |   plots.py
    |   preprocess.py
    |   recorder.py
    |   score.py
    |   search.py
    |   shazir.py
    
```

