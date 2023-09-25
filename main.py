from dependecies import fftLib,functowav
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft,ifft
import math
from scipy.io import wavfile


def filter(fft,cutoff,t):
    filterFft = fft.copy()
    filterFft[np.abs(np.fft.fftfreq(len(t))) > cutoff] = 0
    filteredFft = fft * filterFft
    filteredSignal = ifft(filteredFft)
    return filteredSignal



if __name__ == '__main__':
    startTime = 0.0
    sampleRate = 44100
    func = lambda t, frequency:4 *np.sin((frequency*2*np.pi)*10/np.exp(frequency*t/10))
    import tkinter as tk
    from tkinter import messagebox
    def openOutput():
        import os
        os.startfile("output.wav")
    def generateWavButtonClicked():
        try:
            frequency = float(freq_entry.get())
            duration = float(duration_entry.get())
            cutoff = float(cutoff_entry.get())
            endTime = startTime+duration
            t = np.linspace(startTime, endTime, int((endTime - startTime) * sampleRate), endpoint=False)
            values = func(t, frequency)
            if 0 <= frequency <= 20000 and 0 <= duration <= 60 and cutoff <= 20000:
                fftOfSignal = fftLib.generateFFT(values)
                filteredSignal = filter(fftOfSignal,cutoff,t)
                functowav.generateWav2(filteredSignal)
                messagebox.showinfo("Success", "WAV file generated successfully!")
                openOutput()
            else:
                messagebox.showerror("Error", "Invalid parameter values. Frequency must be in [0, 20 000] and duration in [0, 60] and cutoff in [0, 20 000].")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
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

    root.mainloop()