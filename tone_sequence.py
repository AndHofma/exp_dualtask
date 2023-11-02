import numpy as np
import wavio
import random

# Constants
RATE = 44100    # samples per second
TONE_DURATION = 0.2  # seconds
SILENT_DURATION = 0.4 # seconds
REPETITIONS = 10 # repetitions of each tone

# Generate tone function
def generate_tone(freq, duration):
    # Compute waveform samples
    t = np.linspace(0, duration, int(RATE * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t)

# Generate silence function
def generate_silence(duration):
    return np.zeros(int(RATE * duration))

# Generate tones for C5 and A5
C5 = 523.25  # Frequency in Hz
A5 = 880.00  # Frequency in Hz

tone_C5 = generate_tone(C5, TONE_DURATION)
tone_A5 = generate_tone(A5, TONE_DURATION)

# Create a list with desired number of repetitions for each tone
tones_list = [tone_C5]*REPETITIONS + [tone_A5]*REPETITIONS

# Shuffle the tones randomly
random.shuffle(tones_list)

# Add silence between each tone
tones_with_silences = []
for tone in tones_list:
    tones_with_silences.append(tone)
    tones_with_silences.append(generate_silence(SILENT_DURATION))

# Convert list back to numpy array for saving as WAV
tones_sequence = np.concatenate(tones_with_silences)

# Save to WAV file
wavio.write("tones_C5_A5_random.wav", tones_sequence, RATE, sampwidth=4)
