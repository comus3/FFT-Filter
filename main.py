from dependecies import fftLib,functowav
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft,ifft
import math
from scipy.io import wavfile


def filter(audio_data,cutoff,t):
    audio_fft = fftLib.generateFFT(audio_data)
    frequency_axis = np.fft.fftfreq(len(audio_data))
    filter_fft = np.zeros(len(audio_data), dtype=np.complex128)
    filter_fft[np.abs(frequency_axis) <= cutoff] = 1.0
    
    filtered_audio_fft = audio_fft * filter_fft
    
    filtered_audio_data = np.real(ifft(filtered_audio_fft))

    return filtered_audio_data




if __name__ == '__main__':
    startTime = 0.0
    sampleRate = 44100
    #func = lambda t, frequency:6 * np.sin(t*np.sin(frequency*np.pi*2))
    #func = lambda t, frequency:4 *np.sin((frequency*2*np.pi)*10/np.exp(frequency*t/10))
    func = lambda t , frequency:7*np.tan(np.sin(t*frequency*2*np.pi))
    import tkinter as tk
    from tkinter import messagebox
    def openOutput(file):
        import os
        os.startfile(file)
    def playOriginal():
        try:
            openOutput("original.wav")
        except ValueError:
            messagebox.showerror("Error", "Could not read wav... ):")
    def playFiltered():
        try:
            openOutput("output.wav")
        except ValueError:
            messagebox.showerror("Error", "Could not read wav... ):")

    def generateWavButtonClicked():
        try:
            frequency = float(freq_entry.get())
            duration = float(duration_entry.get())
            cutoff = float(cutoff_entry.get())
            endTime = startTime+duration
            sampleWidth = 4
            t = np.linspace(startTime, endTime, int((endTime - startTime) * sampleRate), endpoint=False)
            values = func(t, frequency)
            if 0 <= frequency <= 20000 and 0 <= duration <= 60 and cutoff <= 20000:
                filteredSignal = filter(values,cutoff,t)
                functowav.generateWavPydub(filteredSignal,sampleWidth,sampleRate)
                functowav.generateWavPydub(values,sampleWidth,sampleRate,"original.wav")
                openOutput()
                messagebox.showinfo("Success", "WAV file generated and played successfully!")
            else:
                messagebox.showerror("Error", "Invalid parameter values. Frequency must be in [0, 20 000] and duration in [0, 60] and cutoff in [0, 20 000].")
        except ValueError:
            messagebox.showerror("Error", "Could not generate wav... ):")
    root = tk.Tk()
    root.title("WAV Generator")

    freq_label = tk.Label(root, text="Frequency (0 to 20 000):")
    freq_label.pack()
    freq_entry = tk.Entry(root)
    freq_entry.pack()

    duration_label = tk.Label(root, text="Duration (0 to 60 seconds):")
    duration_label.pack()
    duration_entry = tk.Entry(root)
    duration_entry.pack()

    cutoff_label = tk.Label(root, text="cutoff frequency(0 to 20 000):")
    cutoff_label.pack()
    cutoff_entry = tk.Entry(root)
    cutoff_entry.pack()



    generate_button = tk.Button(root, text="Generate WAV", command=generateWavButtonClicked)
    generate_button.pack()
    generate_button = tk.Button(root, text="play original", command=playOriginal)
    generate_button.pack()
    generate_button = tk.Button(root, text="play filtered", command=playFiltered)
    generate_button.pack()

    root.mainloop()