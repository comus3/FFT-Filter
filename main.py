import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import tkinter as tk
from tkinter import ttk
from functools import partial
from dependencies import funcLib,functowav

# Global variables to store coefficients
original_coefficients = []
filtered_coefficients = []


class FourierInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        # Input fields
        self.function_var = tk.StringVar(value="np.sin")  # Default function is np.sin
        self.period_start_var = tk.DoubleVar(value=0.0)
        self.period_end_var = tk.DoubleVar(value=2 * np.pi)
        self.wav_start_time_var = tk.DoubleVar(value=0.0)
        self.wav_stop_time_var = tk.DoubleVar(value=5.0)
        self.filter_type_var = tk.StringVar(value="lowpass")  # Default filter type is lowpass
        self.cutoff_frequency_var = tk.DoubleVar(value=2.0)

        # Labels
        ttk.Label(self, text="Function Name:").grid(row=0, column=0, sticky="e")
        ttk.Label(self, text="Period Start:").grid(row=1, column=0, sticky="e")
        ttk.Label(self, text="Period End:").grid(row=2, column=0, sticky="e")
        ttk.Label(self, text="Wav Start Time:").grid(row=3, column=0, sticky="e")
        ttk.Label(self, text="Wav Stop Time:").grid(row=4, column=0, sticky="e")
        ttk.Label(self, text="Filter Type:").grid(row=5, column=0, sticky="e")
        ttk.Label(self, text="Cutoff Frequency:").grid(row=6, column=0, sticky="e")

        # Entry widgets
        ttk.Entry(self, textvariable=self.function_var).grid(row=0, column=1)
        ttk.Entry(self, textvariable=self.period_start_var).grid(row=1, column=1)
        ttk.Entry(self, textvariable=self.period_end_var).grid(row=2, column=1)
        ttk.Entry(self, textvariable=self.wav_start_time_var).grid(row=3, column=1)
        ttk.Entry(self, textvariable=self.wav_stop_time_var).grid(row=4, column=1)
        ttk.Combobox(self, textvariable=self.filter_type_var, values=["lowpass", "highpass"]).grid(row=5, column=1)
        ttk.Entry(self, textvariable=self.cutoff_frequency_var).grid(row=6, column=1)

        # Buttons
        ttk.Button(self, text="Generate Data", command=self.generate_data).grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Generate WAV", command=self.generate_wavs).grid(row=8, column=0, columnspan=2, pady=10)

    def generate_data(self):
        function_name = self.function_var.get()
        period_start = self.period_start_var.get()
        period_end = self.period_end_var.get()
        filter_type = self.filter_type_var.get()
        cutoff_frequency = self.cutoff_frequency_var.get()
        num_of_sines = 10  # You can adjust this value
        func = getattr(funcLib, function_name, np.sin)  # Get the function from funcLib or use np.sin by default
        generateData(func, period_start, period_end, filter_type, cutoff_frequency, num_of_sines)

    def generate_wavs(self):
        start_time = self.wav_start_time_var.get()
        stop_time = self.wav_stop_time_var.get()
        generateWavs(start_time, stop_time)



def integrand_sine(x, n, period_start, period_end, math_function):
    return math_function(x) * np.sin(2 * np.pi * n * (x - period_start) / (period_end - period_start))

def integrand_cosine(x, n, period_start, period_end, math_function):
    return math_function(x) * np.cos(2 * np.pi * n * (x - period_start) / (period_end - period_start))

def fourier_series_coefficients(math_function, numOfSines, period_start, period_end):
    coefficients = []
    for n in range(1, numOfSines + 1):
        # Coefficients for sine and cosine terms
        a_n, _ = quad(integrand_sine, period_start, period_end, args=(n, period_start, period_end, math_function))
        b_n, _ = quad(integrand_cosine, period_start, period_end, args=(n, period_start, period_end, math_function))

        a_n *= 2 / (period_end - period_start)
        b_n *= 2 / (period_end - period_start)

        # Store the coefficients in the list
        coefficients.append({'n': n, 'a_n': a_n, 'b_n': b_n})

    return coefficients

def filter_coefficients(coefficients, filter_type, cutoff_frequency,period_start,period_end):
    filtered = []

    for coef in coefficients:
        frequency = coef['n'] / (period_end - period_start)

        if (filter_type == 'lowpass' and frequency <= cutoff_frequency) or \
           (filter_type == 'highpass' and frequency >= cutoff_frequency):
            filtered.append(coef)

    return filtered

def plot_fourier_series(coefficients, period_start, period_end, num_points=1000):
    x_values = np.linspace(period_start, period_end, num_points)
    result = np.zeros_like(x_values)

    for coef in coefficients:
        result += coef['a_n'] * np.sin(2 * np.pi * coef['n'] * (x_values - period_start) / (period_end - period_start)) + \
                  coef['b_n'] * np.cos(2 * np.pi * coef['n'] * (x_values - period_start) / (period_end - period_start))

    plt.plot(x_values, result, label='Sum of Sines and Cosines')
    plt.legend()
    plt.show()

def generateData(math_function, period_start, period_end, filter_type, cutoff_frequency, numOfSines):
    global original_coefficients
    global filtered_coefficients

    # Compute the Fourier series coefficients for the original function
    original_coefficients = fourier_series_coefficients(math_function, numOfSines, period_start, period_end)

    # Filter the coefficients
    filtered_coefficients = filter_coefficients(original_coefficients, filter_type, cutoff_frequency,period_start,period_end)

    # Plot the original signal
    x_values = np.linspace(period_start, period_end, 1000)
    original_values = math_function(x_values)
    plt.plot(x_values, original_values, label='Original Signal')

    # Plot the Fourier series approximation
    plot_fourier_series(filtered_coefficients, period_start, period_end)

def generateWavs(start_time, end_time):
    global filtered_coefficients

    # Check if filtered_coefficients is empty
    if not filtered_coefficients:
        print("Error: Filtered coefficients are not available. Please run generateData first.")
        return

    # Sample rate
    sample_rate = 44100

    # Create a linspace for the specified time range
    time_values = np.linspace(start_time, end_time, int((end_time - start_time) * sample_rate), endpoint=False)

    # Calculate the values for the original function coefficients
    original_values = np.zeros_like(time_values)
    for coef in filtered_coefficients:
        original_values += coef['a_n'] * np.sin(2 * np.pi * coef['n'] * (time_values - start_time) / (end_time - start_time)) + \
                          coef['b_n'] * np.cos(2 * np.pi * coef['n'] * (time_values - start_time) / (end_time - start_time))

    # Calculate the values for the sum of sines and cosines
    result_values = np.zeros_like(time_values)
    for coef in filtered_coefficients:
        result_values += coef['a_n'] * np.sin(2 * np.pi * coef['n'] * (time_values - start_time) / (end_time - start_time)) + \
                         coef['b_n'] * np.cos(2 * np.pi * coef['n'] * (time_values - start_time) / (end_time - start_time))

    # Save the original values to a WAV file
    functowav.generateWav2(original_values, sample_rate, "original.wav")

    # Save the sum of sines and cosines values to a WAV file
    functowav.generateWav2(result_values, sample_rate, "result.wav")


if __name__ == "__main__":
    app = FourierInterface()
    app.title("Fourier Transform Interface")
    app.mainloop()