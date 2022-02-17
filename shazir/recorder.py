import numpy as np
import librosa
import soundfile as sf
import pyaudio
import tkinter
import tkinter as tk
import tkinter.messagebox
import time
from tkinter import messagebox

class Recorder():
    
    def __init__(self, format_audio = pyaudio.paFloat32, channels = 1,
                 rate = 22050, frames = 2048):
        self._format = format_audio
        self._channels = channels
        self._rate = rate
        self._frames = frames
        self._audio = None
        self._stream = None
        
    def record(self, name = 'recording.wav'):
        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('500x300')
        self.main.title('Record')
        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=120, pady=20)
        # Pack Frame
        self.buttons.pack(fill=tk.BOTH)
        # Start and Stop buttons
        self.start_rec = tkinter.Button(self.buttons, width=20, padx=10,
            pady=5, text='Start Recording', command=lambda: self.start(),
            bg='white')
        self.start_rec.grid(row=0, column=0, padx=50, pady=5)
        self.stop_rec = tkinter.Button(self.buttons, width=20, padx=10,
            pady=5,
            text='Stop Recording', command=lambda: self.stop(), bg='white')
        self.stop_rec.grid(row=1, column=0, columnspan=1, padx=50, pady=5)
        self.stop_rec.configure(state='disabled')

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.main.destroy()

        self.main.protocol("WM_DELETE_WINDOW", on_closing)

        tkinter.mainloop()
        
        try:
            sf.write(name, self._full_data, self._rate)
            self.recording = 'recording.wav'
        except:
            print("Quitting shazir...")
        
        
    def start(self):
        self.start_rec.configure(bg='red', text='Recording...',
            state='disabled')
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(format=self._format,
                                      channels=self._channels,
                                      rate=self._rate,
                                      input=True,
                                      output=False,
                                      stream_callback=self.callback,
                                      frames_per_buffer=self._frames)
    
    def stop(self):
        self._stream.close()
        self._audio.terminate()
        self.main.destroy()
    
    def callback(self, in_data, frame_count, time_info, flag):
        self.stop_rec.configure(state='active')
        numpy_array = np.frombuffer(in_data, dtype=np.float32)
        librosa.feature.mfcc(numpy_array)
        try:
            self._full_data = np.append(self._full_data, numpy_array)
        except:
            self._full_data = numpy_array
        return None, pyaudio.paContinue        

    def get_rate(self):
        return self._rate
    
    def get_recording(self):
        return self._full_data
