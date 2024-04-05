# -*- coding: utf-8 -*-
"""LOAIW_ch02_exploring_audio_data_workflows.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lj895IOyp0OL4RJMk3m6aPZ1w_NcPyp2

# Learn OpenAI Whisper - Chapter 2
## Complementary exploration of audio data workflows and compute optimization for Whisper

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Lj895IOyp0OL4RJMk3m6aPZ1w_NcPyp2)

This notebook is designed to serve as a comprehensive guide for handling and analyzing audio data, with practical examples and explanations tailored to the context of Whisper and automatic speech recognition (ASR).

**Understanding audio signals**

An audio signal is a digital representation of sound waves. When we explore audio processing, especially with Python's Librosa library, we are essentially transforming these sound waves into a format that can be manipulated and analyzed computationally, a crucial step in Whisper's speech recognition process.

Sound waves are vibrations that travel through mediums like air and are captured by our ears, enabling us to perceive sound. In the digital world, these vibrations are captured by microphones, which convert the analog waves into electrical signals. These signals are then digitized, resulting in a digital audio signal that can be stored, transmitted, and processed by computers, like Whisper's ASR system.

The digital audio signal is typically represented as a sequence of numbers, each corresponding to the air pressure at a specific point in time. This sequence, known as a waveform, can be manipulated using various digital signal processing techniques to extract meaningful information or to alter the sound in some way, a process integral to Whisper's operation.

**Introducing Librosa**

[Librosa](https://librosa.org/doc/latest/index.html) is a powerful Python library designed for audio and music analysis. It simplifies the process of working with audio signals by providing a comprehensive toolkit for loading, analyzing, and manipulating these signals. With Librosa, one can perform tasks such as feature extraction, which includes obtaining Mel-frequency cepstral coefficients (MFCCs), spectral contrast, and tonnetz. These features are crucial for various applications in music information retrieval, speech recognition, and audio classification, including Whisper's ASR system.

Working with audio signals in Python using Librosa involves loading the audio file into a NumPy array, which then allows for the application of various processing techniques. Librosa's functionality is not limited to feature extraction; it also includes capabilities for beat tracking, pitch estimation, and creating visual representations of audio signals, such as spectrograms, all of which can be beneficial in the context of Whisper and ASR.

# Load required Python libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install -q cohere openai tiktoken
# !pip install -q librosa
# !pip install -q git+https://github.com/openai/whisper.git

from IPython.display import Audio
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import wave
import librosa
import nltk
nltk.download('punkt')
from nltk import sent_tokenize

"""# Loading sample audio files"""

!wget -nv https://github.com/PacktPublishing/Learn-OpenAI-Whisper/raw/main/Chapter01/Learn_OAI_Whisper_Sample_Audio01.mp3
!wget -nv https://github.com/PacktPublishing/Learn-OpenAI-Whisper/raw/main/Chapter01/Learn_OAI_Whisper_Sample_Audio02.mp3

# Path to the uploaded audio file
audio_file_path = 'Learn_OAI_Whisper_Sample_Audio01.mp3'

# Load the audio file
audio, sampling_frequency = librosa.load(audio_file_path, mono=False)  # You can adjust the sample rate as needed

Audio(audio, rate=sampling_frequency)

"""## Coverting to MP3 to WAV file format"""

import soundfile as sf
audio_file_path = 'Learn_OAI_Whisper_Sample_Audio01.mp3'
audio, sampling_frequency = librosa.load(audio_file_path, mono=True)  # You can adjust the sample rate as needed
sf.write('Learn_OAI_Whisper_Sample_Audio01.wav', audio, sampling_frequency) # Can only convert monoaural files, due to a bug in C library libsndfile version <= 1.0.25

with wave.open('/content/Learn_OAI_Whisper_Sample_Audio01.wav', 'rb') as wav_file:
    channels_number, sample_width, framerate, frames_number, compression_type, compression_name = wav_file.getparams()
    frames = wav_file.readframes(frames_number)
    audio_signal = np.frombuffer(frames, dtype='<i2')

channels_number, sample_width, framerate, frames_number, compression_type, compression_name

Audio(audio_signal, rate=sampling_frequency)

"""# Librosa use cases

## Loading the audio samples using librosa
"""

mono_file = "Learn_OAI_Whisper_Sample_Audio01.mp3"
stereo_file = "Learn_OAI_Whisper_Sample_Audio02.mp3"

mono_signal, sample_rate = librosa.load(mono_file)
stereo_signal, sample_rate = librosa.load(stereo_file, mono=False)

Audio(data=stereo_signal, rate=sample_rate)

Audio(data=mono_signal, rate=sample_rate)

"""## Transcribing with Whisper"""

import whisper

# Load the small English model
model = whisper.load_model("small")

# Transcribe the mono audio file
result = model.transcribe(mono_file)
print("Transcription of mono_file:")
for sent in sent_tokenize(result['text']):
  print(sent)

# Transcribe the stereo audio file
result = model.transcribe(stereo_file)
print("Transcription of stereo_file:")
for sent in sent_tokenize(result['text']):
  print(sent)

"""## Audio sampling

Sampling refers to sample the signal at specific time intervals. Either you can upsample or downsample your audio files based on your requirement.

Original sampling rate is at 44 kHz since we have observed previously. We can upsample or downsample it by **librosa.resample()** function
"""

audio_file = mono_file
# get raw audio features
print("Sampling Rate : "+ str(librosa.get_samplerate(audio_file))+"Hz")
print("Duration : "+ str(librosa.get_duration(path=audio_file))+"s")

# import the audio files
signal, sampling_rate = librosa.load(audio_file, mono=False)
# # Shape of features
print("Shape of Initial Data : "+ str(signal.shape))

# Downsample to 22 kHz
signal_22k = librosa.resample(signal, orig_sr=sampling_rate, target_sr=22000)
# Upsample to 88 kHz
signal_88k = librosa.resample(signal, orig_sr=sampling_rate, target_sr=88000)
print(signal_22k.shape)
print(signal_88k.shape)

"""## Pitch"""

# Load audio file
y, sr = librosa.load(mono_file)

# Compute pitch
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

# Plot pitch contour
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.5)
plt.plot(librosa.frames_to_time(range(len(f0))), f0, color='r')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Pitch Contour')
plt.show()
Audio(y, rate=sr)

"""## Pitch shift"""

# Shift the pitch down by two semitones
pitch_shifted_waveform = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=-4.0)
Audio(pitch_shifted_waveform, rate=sr)

# Normalize the output signal
pitch_shifted = librosa.util.normalize(pitch_shifted_waveform)
Audio(pitch_shifted, rate=sr)

# Shift the pitch up by five semitones
pitch_shifted_helium_voice = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=6.0)
Audio(pitch_shifted_helium_voice, rate=sr)

"""## Time stretch

"""

# Stretch the time by a factor of 2
time_stretched_waveform = librosa.effects.time_stretch(pitch_shifted_helium_voice, rate=2)
Audio(time_stretched_waveform, rate=sr)

"""## Beats generation"""

# Set the parameters for the audio file
duration = 2.0  # seconds
frequency = 440.0  # Hz (A440)
sample_rate = 22050  # Hz

# Calculate the number of samples
num_samples = int(duration * sample_rate)

# Generate the tone
data = librosa.tone(frequency, sr=sample_rate, length=num_samples)

Audio(data, rate=sample_rate)

"""## Audio channels
There are two main types of audios as Monophonic (mono) and Stereophonic (stereo) sound. It classified based on the number of channels used to record and playback audio. But there can be more than two channels as well.
Stereo sounds are much advance and it enables to localize the data which easy to locate the position of a sound source within a space.Usually we used mono channel audio for preprocessing tasks since it is complex to analyze high-dimensional data.

Number of channels can be viewed by **.shape** attribute of the audio signal and librosa has an inbuilt function to convert into mono channel.

As in the above example, original audio file is in stereo format as it is in **(2, 422400)** format. By converting it into mono, it takes the average of each channel and creates a new signal.
"""

print(stereo_signal.shape)# Initially the signal is in stereo form (2 channels)
audio_mono = librosa.to_mono(signal)
print(audio_mono.shape) # Mono signal

"""## Plotting the signal amplitude

**librosa.display** gives a high level representation of the audio in time domain with amplitude in the y axis.
"""

import librosa.display

plt.figure(figsize=(10, 3))
librosa.display.waveshow(mono_signal, sr=sample_rate) # use waveplot should waveshow be unavailable
plt.show()

""" Modifying the script to handle both stereo and mono audio signals is a great approach for flexibility. The script will first check if the input is a stereo signal. If it is, it will plot both channels. If it's a mono signal, it will just plot that single channel. Here's the revised script:"""

import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Use commenting/uncommenting to see the plots
#audio_signal_to_plot = mono_signal
audio_signal_to_plot = stereo_signal

# Ensure audio_signal_to_plot is a NumPy array
audio_signal_to_plot = np.array(audio_signal_to_plot)

# Check if audio_signal_to_plot is a stereo signal
if audio_signal_to_plot.ndim == 2 and audio_signal_to_plot.shape[0] == 2:
    # Two channels, each row is a channel
    channel_1, channel_2 = audio_signal_to_plot
    is_stereo = True
elif audio_signal_to_plot.ndim == 2 and audio_signal_to_plot.shape[1] == 2:
    # Two channels, each column is a channel
    channel_1, channel_2 = audio_signal_to_plot.T
    is_stereo = True
else:
    # It's a mono signal
    is_stereo = False

# Plotting
if is_stereo:
    plt.figure(figsize=(10, 6))
    # Plotting the first channel
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(channel_1, sr=sample_rate)
    plt.title('Channel 1')
    # Plotting the second channel
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(channel_2, sr=sample_rate)
    plt.title('Channel 2')
    plt.tight_layout()
else:
    plt.figure(figsize=(10, 3))
    librosa.display.waveshow(audio_signal_to_plot, sr=sample_rate)
    plt.title('Mono Audio Signal')

plt.show()

"""## Time domain vs frequency domain

As you observe in the previous diagram, it is much complex to take a greater understanding about the **.mp3** file features from the raw audio waveplot. The reason is, it visulized in time domain and no any mathematical representation is available. On the contray, frequency domain delivers lot more understanding via decomping complex waves as a sum of sine wave oscillations. This operation often known as **Fourier Transformation**.

### Fast-fourier transformation (FFT)

This will result a **spectrum** as time is in x-axis and frequency is in y-axis. **Discrete fourier transformation** or DFT is transform digital signal into frequency representation. But, FFT is widely used as an efficient fourier transformation technique for audio processing. It takes the DFT and its inverse by factorization into sparse matrix.
"""

audio = mono_signal
# Calculate the Fourier transform of the signal
fft = np.fft.fft(audio)
# Calculate absolute values on complex numbers to get magnitude
spectrum = np.abs(fft)
# Create frequency variable
f = np.linspace(0, sr, len(spectrum))
# Take half of the spectrum and frequency
left_spectrum = spectrum[:int(len(spectrum)/2)]
left_f = f[:int(len(spectrum)/2)]

# Plot spectrum
plt.figure(figsize=(9,6))
plt.plot(left_f, left_spectrum, alpha=0.4)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.title("Power spectrum")
plt.show()

"""### Short-time fourier transform (STFT)

In FFT, we lose time information when we are converting from time domain to frequency domain representation. As a remedy, STFT can be applied.

The n_fft value is the length of the windowed signal after padding with zeros. The number of rows in the STFT matrix D is (1 + n_fft/2).
The default value, n_fft=2048 samples, corresponds to a physical duration of 93 milliseconds at a sample rate of 22050 Hz,
i.e. the default sample rate in librosa. This value is well adapted for music signals.

However, in speech processing, the recommended value is 512, corresponding to 23 milliseconds at a sample rate of 22050 Hz.
In any case, we recommend setting n_fft to a power of two for optimizing the speed of the fast Fourier transform (FFT) algorithm.

Thus, we are keeping n_fft as 512 since this is for speech processing. The value will change throughout the code notebook going forward.
"""

audio = mono_signal
n_fft = 512

'''
Short-time Fourier transform (STFT).
The STFT represents a signal in the time-frequency domain by
computing discrete Fourier transforms (DFT) over short overlapping
windows.
'''

ft = np.abs(librosa.stft(audio[:n_fft], n_fft=n_fft, hop_length = n_fft+1))

plt.figure(figsize=(12, 4))
plt.plot(ft);
plt.title('Spectrum');
plt.xlabel('Frequency Bin');
plt.ylabel('Amplitude');

# load audio file
audio_file = mono_file

signal, sample_rate = librosa.load(audio_file, sr=22050)

hop_length = 512 # In num. of samples
n_fft = 512 # Window in num. of samples

# Calculate duration hop length and window in seconds
hop_length_duration = float(hop_length)/sample_rate
n_fft_duration = float(n_fft)/sample_rate
print("STFT hop length duration is: {}s".format(hop_length_duration))
print("STFT window duration is: {}s".format(n_fft_duration))

# Perform stft and take the absolute value
spectrogram = np.abs(librosa.stft(signal, n_fft=n_fft, hop_length=hop_length))

# Display spectrogram
librosa.display.specshow(spectrogram, sr=sample_rate, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()
plt.title("Spectrogram")
plt.show()

"""Above plot not gonna display much information (very tiny area is visible). Reason is human auditory space is very thin and most sounds humans hear are concentrated in very small frequency and amplitude ranges. A small adjustment will display more discriptive view of spectrum as below.

## Spectral features

Spectral features capture the frequency domain representation of an audio signal, providing information about the different frequency components present in the signal. They help to capture the timbre and texture of sounds and the energy distribution across different frequency bands. This information is vital in ASR systems like Whisper, as it helps to distinguish between different phonemes, the smallest units of sound that can distinguish one word from another in a particular language.

**Librosa** provides easy-to-use functions for computing spectral features. It offers multiple options for spectral feature extraction, including the mel-spectrogram and its coefficients, and Chroma features. These features are particularly useful in ASR as they provide a compact representation of the spectral content of the audio signal, emphasizing various aspects of the signal, such as its harmonic or percussive content.

In the context of ***Whisper***, these spectral features can be used to improve the accuracy of speech recognition. By analyzing the spectral content of the audio signal, Whisper can better understand the nuances of spoken language, making it more robust to variations in speech such as accents, speech speed, and background noise. This allows Whisper to convert spoken language into written text more accurately, making it a valuable tool for transcribing audio files
"""

# Magnitude scaling of an amplitude spectrogram to dB-scaled spectrogram.
DB = librosa.amplitude_to_db(spectrogram, ref=np.max)
librosa.display.specshow(DB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log');
plt.colorbar(format='%+2.0f dB');
plt.title("Spectrogram (dB)")

"""Above representation known as **spectrogram**. As display in the code, we applied logarithm to cast amplitude to Decible (DB) scale for previously compute stft spectrogram. As you may have understood, STFT produce by computing FT at different intervals. By doing so it preseves the time dimension information.

This STFT information is an essential input for any deep learning based model.

### The mel-spectrogram

The mel-spectrogram is a pivotal feature in the domain of audio and music analysis, and its utility extends to the sophisticated tasks of sound classification and automatic speech recognition (ASR), such as those performed by OpenAI's Whisper. This spectral representation is adept at encapsulating the timbral and textural nuances of sounds, as well as delineating the energy distribution across various frequency bands.

In the realm of ASR, the mel-spectrogram serves as a foundational input, providing a rich, condensed depiction of the audio signal's spectral content. This is particularly beneficial for Whisper, which requires a detailed frequency analysis to accurately transcribe spoken language into written text. The mel-spectrogram's emphasis on the perceptually relevant mel scale aligns closely with human auditory processing, making it an effective tool for capturing the essential characteristics of speech.

To compute a mel-spectrogram, one can utilize the `librosa.feature.melspectrogram` function, which processes the audio signal and yields a two-dimensional array representing the power spectrum of sound across mel frequency bands. This can then be visualized using `librosa.display.specshow`, offering insights into the signal's structure that are instrumental for Whisper's learning algorithms.

The mel-spectrogram's ability to abstract and highlight salient features of the audio signal makes it an indispensable component in Whisper's ASR system. By leveraging this representation, Whisper can enhance its performance, particularly in challenging acoustic environments with noise, multiple speakers, or diverse accents, thereby solidifying its position as a robust and versatile speech recognition tool.
"""

# Load the recorded file
signal, sr = librosa.load(mono_file)

# Compute the mel-spectrogram
mel_spectrogram = librosa.feature.melspectrogram(y=signal, sr=sr)

# Plot the mel-spectrogram
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.power_to_db(mel_spectrogram, ref=np.max), sr=sr, hop_length=512, y_axis="mel", x_axis="time")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-spectrogram")
plt.tight_layout()
plt.show()

"""Now, let's modify the script so that it displays two plots – one for each audio file, "mono_file" and "stereo_file" – we need to load each file separately, compute their respective mel-spectrograms, and then plot them in separate subplots. In this script:

* Each audio file is loaded separately, and their mel-spectrograms are computed.
* "**plt.subplot(2, 1, 1)**" and "**plt.subplot(2, 1, 2)**" are used to create two subplots in a single column.
* The mel-spectrograms of **"mono_file"** and **"stereo_file"** are displayed in the first and second subplots, respectively.
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load the first file
signal_1, sr_1 = librosa.load(mono_file)

# Compute the mel-spectrogram for the first file
mel_spectrogram_1 = librosa.feature.melspectrogram(y=signal_1, sr=sr_1)

# Load the second file
signal_2, sr_2 = librosa.load(stereo_file)

# Compute the mel-spectrogram for the second file
mel_spectrogram_2 = librosa.feature.melspectrogram(y=signal_2, sr=sr_2)

# Create a figure for the subplots
plt.figure(figsize=(20, 8))

# Plot the mel-spectrogram of the first file
plt.subplot(2, 1, 1)
librosa.display.specshow(librosa.power_to_db(mel_spectrogram_1, ref=np.max), sr=sr_1, hop_length=512, y_axis="mel", x_axis="time")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-spectrogram of mono File")
plt.tight_layout()

# Plot the mel-spectrogram of the second file
plt.subplot(2, 1, 2)
librosa.display.specshow(librosa.power_to_db(mel_spectrogram_2, ref=np.max), sr=sr_2, hop_length=512, y_axis="mel", x_axis="time")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-spectrogram of Stereo File")
plt.tight_layout()

plt.show()

"""You might be asking, "...is there a way we can represent both channels of the stereo file in the mel-spectogram?"

Surely! Although representing a stereo, 2-channel audio file in a mel-spectrogram involves a decision on how to handle the two channels. There are a few approaches:

* **Average the Channels**: Compute the mel-spectrogram of the average of the two channels. This approach merges the stereo information into a single representation.
* **Separate Spectrograms for Each Channel**: Compute and display separate mel-spectrograms for each channel.
* **Sum the Channels**: Another method is to sum the channels before computing the mel-spectrogram, although this can sometimes lead to a loss of stereo-specific information.

For most analysis purposes, the second approach (separate spectrograms for each channel) is often more informative as it maintains the distinct information from each channel. Here's how you can modify the script to handle a stereo file and plot separate mel-spectrograms for each channel of the "stereo_file":
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load the first file (mono)
signal_1, sr_1 = librosa.load(mono_file)

# Compute and plot the mel-spectrogram for the first file
mel_spectrogram_1 = librosa.feature.melspectrogram(y=signal_1, sr=sr_1)
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.power_to_db(mel_spectrogram_1, ref=np.max), sr=sr_1, hop_length=512, y_axis="mel", x_axis="time")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-spectrogram of mono File")
plt.tight_layout()
plt.show()

# Load the second file (stereo)
signal_2, sr_2 = librosa.load(stereo_file, mono=False)

# Assuming the stereo signal has two channels
channel_1, channel_2 = signal_2

# Compute and plot the mel-spectrogram for each channel of the stereo file
plt.figure(figsize=(10, 8))

# Channel 1
mel_spectrogram_2_1 = librosa.feature.melspectrogram(y=channel_1, sr=sr_2)
plt.subplot(2, 1, 1)
librosa.display.specshow(librosa.power_to_db(mel_spectrogram_2_1, ref=np.max), sr=sr_2, hop_length=512, y_axis="mel", x_axis="time")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-spectrogram of Stereo File (Channel 1)")
plt.tight_layout()

# Channel 2
mel_spectrogram_2_2 = librosa.feature.melspectrogram(y=channel_2, sr=sr_2)
plt.subplot(2, 1, 2)
librosa.display.specshow(librosa.power_to_db(mel_spectrogram_2_2, ref=np.max), sr=sr_2, hop_length=512, y_axis="mel", x_axis="time")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-spectrogram of Stereo File (Channel 2)")
plt.tight_layout()

plt.show()

"""### Mel-frequency cepstral coefficient (MFCC)

Mel-frequency cepstral coefficients (MFCCs) are a widely recognized feature set used in the field of automatic speech recognition, including in advanced systems like OpenAI's Whisper. These coefficients provide a compact representation of the power spectrum of an audio signal, emphasizing the perceptual and phonetic characteristics that are crucial for distinguishing between different spoken words and sounds.

The process of computing MFCCs involves several steps. First, the audio signal is passed through a mel-scale filter bank, which mimics the human ear's response to different frequencies. The logarithm of the powers at each of the mel frequencies is then taken, and a discrete cosine transform (DCT) is applied to the log-mel spectrum. This results in a set of coefficients that succinctly capture the essential information needed for speech recognition tasks.

MFCCs are particularly useful for Whisper's deep learning models, as they encapsulate the relevant features that differentiate one phoneme from another. By incorporating MFCCs into its input features, Whisper can effectively train its neural networks to recognize patterns in speech, leading to more accurate transcriptions.

The robustness of MFCCs in various acoustic environments makes them a staple in Whisper's toolkit for processing and understanding human speech. Their ability to capture the nuances of spoken language enables Whisper to perform with high precision across diverse datasets and in real-world scenarios where background noise and different accents are present.
"""

hop_length = 512 # In num. of samples
n_fft = 512 # Window in num. of samples
audio = mono_signal

# Extract 8 MFCCs
# MFCC = librosa.feature.mfcc(audio, sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=8)
MFCC = librosa.feature.mfcc(y=audio, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=8)

plt.figure(figsize=(9,6))
librosa.display.specshow(MFCC, sr=sr, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("MFCC coefficients")
plt.colorbar()
plt.title("MFCCs")
plt.show()

"""## Spectral Contrast

Spectral contrast is a significant feature in the realm of audio signal processing, and it plays a crucial role in automatic speech recognition systems like OpenAI's Whisper. This feature quantifies the disparity in amplitudes between neighboring frequency bands within a power spectrum, providing a measure of the perceived "brightness" or "spectral shape" of an audio signal.

In Whisper's context, spectral contrast can help differentiate between various phonetic elements in speech, as different sounds will exhibit different spectral shapes. This differentiation is vital for accurately transcribing spoken language into written text.

The computation of spectral contrast involves dividing the audio signal's frequency spectrum into multiple frequency bands, typically using a logarithmic scale. The mean magnitude of the frequency spectrum within each sub-band is then computed, followed by the calculation of the standard deviation of the magnitudes across all sub-bands.

Python's Librosa library provides the `spectral_contrast` function to compute this feature. By incorporating spectral contrast into its feature set, Whisper can enhance its ability to recognize and transcribe speech, even in challenging acoustic environments with background noise or multiple speakers. This makes spectral contrast a valuable tool in Whisper's toolkit for processing and understanding human speech.
"""

# Compute the spectral contrast features
spectral_contrast = librosa.feature.spectral_contrast(y=mono_signal, n_fft=512, hop_length=512)

# Plot the spectral contrast features
plt.figure(figsize=(10, 4))
librosa.display.specshow(spectral_contrast, sr=sample_rate, hop_length=512, x_axis="time")
plt.title("Spectral contrast features")
plt.tight_layout()
plt.show()

"""### Chroma features

Chroma features encapsulate the harmonic content of an audio signal, providing a compact representation that can be used for various audio and music analysis tasks.

Chroma features can help distinguish between different phonetic elements in speech, as different sounds will exhibit different harmonic structures. This differentiation is vital for accurately transcribing spoken language into written text.

The computation of chroma features involves mapping the spectrum of an audio signal to 12 bins representing the 12 distinct semitones (or chroma) of the musical octave. This process effectively captures the pitch content of the audio signal, disregarding the absolute frequency.

Python's Librosa library provides the `chroma_stft` function to compute these features. By incorporating chroma features into its feature set, Whisper can enhance its ability to recognize and transcribe speech, even in challenging acoustic environments with background noise or multiple speakers. This makes chroma features a valuable tool in Whisper's toolkit for processing and understanding human speech.
"""

# Compute the chroma features
chroma_features = librosa.feature.chroma_stft(y=mono_signal, sr=sample_rate)

# Plot the chroma features
plt.figure(figsize=(10, 4))
librosa.display.specshow(chroma_features, sr=sample_rate, hop_length=512, x_axis="time", y_axis="chroma")
plt.title("Chroma features")
plt.tight_layout()
plt.show()

"""# Recap

In this hands-on notebook, we explored practical techniques for loading, sampling, visualizing, and analyzing audio data using Python's Librosa library. We covered audio ingestion fundamentals relevant to preprocessing pipelines in ASR systems like Whisper, including:

* Loading audio files and converting between formats
* Resampling signals to different rates
* Plotting waveforms and spectrograms
* Feature extraction with MFCCs, chroma features etc.
* bAudio effects like pitch shifting and time stretching
* We also demonstrated monitoring performance metrics like Word Error Rate and guidelines for deployment optimization across environments - from on-device to cloud infrastructure.

These audio data processing workflows and compute best practices complement the foundational concepts introduced in Chapter 2. Together, they provide end-to-end coverage - connecting the core ideas around Whisper's architecture with the hands-on application of those principles for tasks like managing data flows and maximizing efficiency.

After this overview spanning theory and practice, you now have an integrated understanding of Whisper's internals alongside applied skills for configuring, deploying, and troubleshooting Whisper-based speech recognition systems. We covered everything from architecture diagrams to practical monitoring and infrastructure provisioning guidelines.

With this rounded foundation, you can now confidently unlock Whisper's capabilities across diverse usage contexts. Optimizing these systems requires blending conceptual, mathematical, and coding proficiency - all gathered over our journey so far.

As we continue our learning voyage in subsequent chapters, we'll further expand on these optimization techniques while exploring additional promising directions with Whisper's capabilities. Our next chapter surveys cutting-edge advancements like multitask learning, robustness to diverse languages and noise conditions, and semi-supervised strategies for accurate speech recognition with limited labeled data.

I'm excited for us to continue discovering together!

## Just for fun!
"""

import librosa
from IPython.display import Audio
import numpy as np

# Frequencies for the scale C3 to C4
note_frequencies = {
    'C3': 130.81,
    'D3': 146.83,
    'E3': 164.81,
    'F3': 174.61,
    'G3': 196.00,
    'A3': 220.00,
    'B3': 246.94,
    'C4': 261.63
}

sample_rate = 22050  # Sample rate in Hz
duration = 0.5       # Duration of each note in seconds

# Create a list to hold the audio data for each note
scale_data = []

# Generate a tone for each note and append to the scale_data
for note, freq in note_frequencies.items():
    tone = librosa.tone(freq, sr=sample_rate, length=int(sample_rate * duration))
    scale_data.append(tone)

# Concatenate all the notes to form the scale
scale = np.concatenate(scale_data)

# Play the scale
Audio(scale, rate=sample_rate)

import librosa
from IPython.display import Audio
import numpy as np

# Mapping notes to frequencies (in Hz)
note_frequencies = {
    'A4': 440.0,
    'D5': 587.33,
    'F4': 349.23,
    'G4': 392.00,
    'D4': 293.66,
    'C5': 523.25,
    'E4': 329.63,
    'C4': 261.63
}

# Beats per minute
bpm = 120
# Duration of one beat in seconds
beat_duration = 60 / bpm

# Theme song notes and durations (note x duration)
theme_song = [
    ('A4', 0.25), ('D5', 0.25), ('A4', 0.25), ('D5', 0.25), ('A4', 2), ('F4', 1),
    ('G4', 1), ('D4', 3),
    ('A4', 0.25), ('D5', 0.25), ('A4', 0.25), ('D5', 0.25), ('A4', 2), ('F4', 1),
    ('G4', 1), ('C5', 3),
    ('A4', 0.25), ('D5', 0.25), ('A4', 0.25), ('D5', 0.25), ('A4', 2), ('F4', 1),
    ('E4', 0.5), ('D4', 0.5), ('C4', 3),
    ('A4', 0.25), ('D5', 0.25), ('A4', 0.25), ('D5', 0.25), ('A4', 2), ('G4', 1),
    ('D4', 1), ('C4', 3)
]

# Sample rate
sample_rate = 22050

# Create a list to hold the audio data for each note
scale_data = []

# Generate a tone for each note and append to the scale_data
for note, duration in theme_song:
    freq = note_frequencies[note]
    tone_duration = duration * beat_duration
    num_samples = int(sample_rate * tone_duration)
    tone = librosa.tone(freq, sr=sample_rate, length=num_samples)
    scale_data.append(tone)

# Concatenate all the notes to form the theme song
theme = np.concatenate(scale_data)

# Play the theme song
Audio(theme, rate=sample_rate)

"""# Gratitude

Thanks to Naval Katoch, [Sahan Dissanayaka](https://sahandisa.github.io/), [Elena Daehnhardt](https://github.com/edaehn/) and [GeeksForGeeks](https://www.geeksforgeeks.org/) for their valuable insights.
"""