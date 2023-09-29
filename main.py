from dependecies import fftLib,functowav,funcLib
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft
import tkinter as tk
from tkinter import messagebox



def filter(audio_data,cutoff,t):
    cutoff = cutoff/20000
    audio_fft = fftLib.generateFFT(audio_data)
    #fftLib.plotFFT(audio_fft)
    frequency_axis = np.fft.fftfreq(len(audio_data))
    filter_fft = np.zeros(len(audio_data), dtype=np.complex128)
    filter_fft[np.abs(frequency_axis) <= cutoff] = 1.0
    filter_fft[np.abs(frequency_axis) >= cutoff] = np.abs(frequency_axis)*0.5
    plotFilter(filter_fft,frequency_axis)
    filtered_audio_fft = audio_fft * filter_fft
    #fftLib.plotFFT(filtered_audio_fft)
    filtered_audio_data = np.real(ifft(filtered_audio_fft))
    return filtered_audio_data
def plotFilter(filter,frequency_axis):
    plt.plot(frequency_axis,np.abs(filter))
    plt.xlabel('Fz')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.title('filter shape')
    plt.show()

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
def plotSignals():
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))

    # Subplot 1: Original Signal
    plt.subplot(2, 1, 1)
    plt.plot(t, values, label='Original Signal', color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Original Signal')
    plt.grid(True)
    plt.legend()

    # Subplot 2: Filtered Signal
    plt.subplot(2, 1, 2)
    plt.plot(t, filteredSignal, label='Filtered Signal', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Filtered signal')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
def generateWavButtonClicked():
    try:
        global values
        global filteredSignal
        global t
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
            messagebox.showinfo("Success", "WAV file generated and played successfully!")
        else:
            messagebox.showerror("Error", "Invalid parameter values. Frequency must be in [0, 20 000] and duration in [0, 60] and cutoff in [0, 20 000].")
    except OSError as err:
        print("OS error:", err)
    except ValueError as err:
        print("Caught a valuer error: ", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


if __name__ == '__main__':
    global sampleRate
    startTime = 0.0
    sampleRate = 44100
    func = funcLib.sineSum
    
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
    generate_button = tk.Button(root, text="show signals", command=plotSignals)
    generate_button.pack()

    root.mainloop()