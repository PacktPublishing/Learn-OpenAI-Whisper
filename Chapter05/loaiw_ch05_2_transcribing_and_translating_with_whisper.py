# -*- coding: utf-8 -*-
"""LOAIW_ch05_2_transcribing_and_translating_with_Whisper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iAkLCMvhRcU50HM0AzY3pjgtE2RS65tR

# Learn OpenAI Whisper - Chapter 5
## Notebook 2: Transcribing and translating with Whisper

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1iAkLCMvhRcU50HM0AzY3pjgtE2RS65tR)

This notebook provides a comprehensive guide for using OpenAI's Whisper model for multilingual automatic speech recognition (ASR) and translation. It's tailored for anyone eager to dive into the capabilities of Whisper, particularly in handling diverse languages. Here's a breakdown of its purpose, the steps involved, and the benefits it offers:

### Purpose:
- **Demonstrate Whisper's Installation and Usage:** Shows how to set up Whisper in a Python environment, including the installation of necessary libraries.
- **Multilingual ASR and Translation:** Illustrates how to perform speech recognition and translation across various languages using Whisper.
- **Dataset Handling:** Utilizes the Fleurs dataset for demonstrating Whisper's capabilities on multilingual audio data.
- **Interactive Demonstration:** Incorporates an interactive Gradio interface, allowing users to experiment with Whisper's transcription and translation features on selected audio samples.

### High-Level Steps:
1. **Installation:** Installs Whisper and other required Python packages like `librosa`, `gradio`, and `kaleido` for audio processing, visualization, and creating interactive web apps.
2. **Environment Setup:** Prepares the Python environment, including handling potential compatibility issues (e.g., with TensorFlow in Colab) and setting up the device for computation.
3. **Dataset Loading:** Provides a widget for selecting a language from the Fleurs dataset, demonstrating how to dynamically work with multilingual data.
4. **Data Preprocessing:** Implements a custom `Fleurs` class to download, extract, and preprocess audio files from the selected language dataset.
5. **Whisper Model Loading and Inference:** Loads the Whisper model, runs it on the dataset to perform transcription and translation, and collects the results.
6. **Interactive Exploration with Gradio:** Sets up a Gradio interface to allow users to interactively select audio samples, adjust inference parameters, and view the ASR and translation results alongside the original audio.

### Benefits:
- **Practical Learning:** By following this code, learners can gain hands-on experience with one of the most advanced ASR and translation models available, understanding both its strengths and limitations across different languages.
- **Interactive Experience:** The inclusion of Gradio for interactive exploration makes it easy for readers to experiment with various settings and hear the outcomes directly, enhancing the learning experience.
- **Comprehensive Approach:** This example covers the entire workflow from data preparation to model inference and result visualization, providing a solid foundation for building similar applications.
- **Multilingual Support:** Demonstrates Whisper's multilingual capabilities, offering insights into working with non-English audio data, which is invaluable for global applications and research.

This guide is an excellent starting point for anyone interested in exploring the intersection of speech processing and machine learning, offering practical insights into using OpenAI's Whisper model effectively.

# Installing Whisper

The commands below will install the Python packages needed to use Whisper models and evaluate the transcription results.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install -q cohere openai tiktoken
# !pip install -q librosa
# !pip install git+https://github.com/openai/whisper.git
# !pip install gradio kaleido

import io
import os
import numpy as np

try:
    import tensorflow  # required in Colab to avoid protobuf compatibility issues
except ImportError:
    pass

import torch
import pandas as pd
import urllib
import tarfile
import whisper
import torchaudio

from scipy.io import wavfile
from tqdm.notebook import tqdm

pd.options.display.max_rows = 100
pd.options.display.max_colwidth = 1000
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

"""# Loading the Fleurs dataset

Select the language of the FLEURS dataset to download. Please note that the transcription and translation performance varies widely depending on the language.

[**FLEURS**](https://arxiv.org/abs/2205.12446) stands for **Few-shot Learning Evaluation of Universal Representations of Speech**. It's a benchmark designed to evaluate the performance of universal speech representations in a **few-shot learning** scenario.

Here are the key details about FLEURS:

- **Dataset**: FLEURS is an **n-way parallel speech dataset** that spans **102 languages**. It is built on top of the machine translation benchmark called **FLoRes-101**.
- **Speech Supervision**: Each language in FLEURS has approximately **12 hours of speech supervision**.
- **Tasks**: FLEURS can be used for various speech-related tasks, including:
    - **Automatic Speech Recognition (ASR)**: Converting spoken language into text.
    - **Speech Language Identification (Speech LangID)**: Identifying the language spoken in an audio clip.
    - **Translation and Retrieval**: Leveraging universal speech representations for translation and retrieval tasks.

The goal of FLEURS is to enable speech technology in more languages and catalyze research in **low-resource speech understanding**
"""

import ipywidgets as widgets

languages = {"af_za": "Afrikaans", "am_et": "Amharic", "ar_eg": "Arabic", "as_in": "Assamese", "az_az": "Azerbaijani",
             "be_by": "Belarusian", "bg_bg": "Bulgarian", "bn_in": "Bengali", "bs_ba": "Bosnian", "ca_es": "Catalan", "cmn_hans_cn": "Chinese",
             "cs_cz": "Czech", "cy_gb": "Welsh", "da_dk": "Danish", "de_de": "German", "el_gr": "Greek", "en_us": "English", "es_419": "Spanish",
             "et_ee": "Estonian", "fa_ir": "Persian", "fi_fi": "Finnish", "fil_ph": "Tagalog", "fr_fr": "French", "gl_es": "Galician", "gu_in": "Gujarati",
             "ha_ng": "Hausa", "he_il": "Hebrew", "hi_in": "Hindi", "hr_hr": "Croatian", "hu_hu": "Hungarian", "hy_am": "Armenian", "id_id": "Indonesian", "is_is": "Icelandic",
             "it_it": "Italian", "ja_jp": "Japanese", "jv_id": "Javanese", "ka_ge": "Georgian", "kk_kz": "Kazakh", "km_kh": "Khmer", "kn_in": "Kannada", "ko_kr": "Korean",
             "lb_lu": "Luxembourgish", "ln_cd": "Lingala", "lo_la": "Lao", "lt_lt": "Lithuanian", "lv_lv": "Latvian", "mi_nz": "Maori", "mk_mk": "Macedonian",
             "ml_in": "Malayalam", "mn_mn": "Mongolian", "mr_in": "Marathi", "ms_my": "Malay", "mt_mt": "Maltese", "my_mm": "Myanmar", "nb_no": "Norwegian",
             "ne_np": "Nepali", "nl_nl": "Dutch", "oc_fr": "Occitan", "pa_in": "Punjabi", "pl_pl": "Polish", "ps_af": "Pashto", "pt_br": "Portuguese", "ro_ro": "Romanian",
             "ru_ru": "Russian", "sd_in": "Sindhi", "sk_sk": "Slovak", "sl_si": "Slovenian", "sn_zw": "Shona", "so_so": "Somali", "sr_rs": "Serbian", "sv_se": "Swedish",
             "sw_ke": "Swahili", "ta_in": "Tamil", "te_in": "Telugu", "tg_tj": "Tajik", "th_th": "Thai", "tr_tr": "Turkish", "uk_ua": "Ukrainian", "ur_pk": "Urdu", "uz_uz": "Uzbek",
             "vi_vn": "Vietnamese", "yo_ng": "Yoruba"}
selection = widgets.Dropdown(
    options=[("Select language", None), ("----------", None)] + sorted([(f"{v} ({k})", k) for k, v in languages.items()]),
    value="ko_kr",
    description='Language:',
    disabled=False,
)

selection

lang = selection.value
language = languages[lang]

assert lang is not None, "Please select a language"
print(f"Selected language: {language} ({lang})")

def download(url: str, target_path: str):
    with urllib.request.urlopen(url) as source, open(target_path, "wb") as output:
        with tqdm(total=int(source.info().get("Content-Length")), ncols=80, unit='iB', unit_scale=True, unit_divisor=1024) as loop:
            while True:
                buffer = source.read(8192)
                if not buffer:
                    break

                output.write(buffer)
                loop.update(len(buffer))


class Fleurs(torch.utils.data.Dataset):
    """
    A simple class to wrap Fleurs and subsample a portion of the dataset as needed.
    """
    def __init__(self, lang, split="test", subsample_rate=1, device=DEVICE):
        url = f"https://storage.googleapis.com/xtreme_translations/FLEURS102/{lang}.tar.gz"
        tar_path = os.path.expanduser(f"~/.cache/fleurs/{lang}.tgz")
        os.makedirs(os.path.dirname(tar_path), exist_ok=True)

        if not os.path.exists(tar_path):
            download(url, tar_path)

        all_audio = {}
        with tarfile.open(tar_path, "r:gz") as tar:
            for member in tar.getmembers():
                name = member.name
                if name.endswith(f"{split}.tsv"):
                    # Ensure you're using the correct method to read the TSV file.
                    # Just make sure it properly handles the TSV data.
                    labels = pd.read_table(tar.extractfile(member), names=("id", "file_name", "raw_transcription", "transcription", "_", "num_samples", "gender"))

                if f"/{split}/" in name and name.endswith(".wav"):
                    audio_bytes = tar.extractfile(member).read()
                    # all_audio[os.path.basename(name)] = wavfile.read(io.BytesIO(audio_bytes))[1]
                    # Use io.BytesIO to create a buffer from the audio bytes
                    # and scipy.io.wavfile.read to read from this buffer.
                    try:
                        rate, data = wavfile.read(io.BytesIO(audio_bytes))
                        all_audio[os.path.basename(name)] = data
                    except ValueError as e:
                        print(f"Error reading {name}: {e}")

        self.labels = labels.to_dict("records")[::subsample_rate]
        self.all_audio = all_audio
        self.device = device

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, item):
        record = self.labels[item]
        audio = torch.from_numpy(self.all_audio[record["file_name"]].copy())
        text = record["transcription"]

        return (audio, text)

dataset = Fleurs(lang, subsample_rate=5)  # subsample 5% of the dataset for a quick demo

"""# Running inference on the dataset using a "medium" size Whisper model

The following will take a few minutes to transcribe and translate utterances in the dataset.
"""

model = whisper.load_model("medium")
print(
    f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
    f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
)

options = dict(language=language, beam_size=5, best_of=5, temperature=0)
transcribe_options = dict(task="transcribe", **options)
translate_options = dict(task="translate", **options)

references = []
transcriptions = []
translations = []

for audio, text in tqdm(dataset):
    transcription = model.transcribe(audio, **transcribe_options)["text"]
    translation = model.transcribe(audio, **translate_options)["text"]

    transcriptions.append(transcription)
    translations.append(translation)
    references.append(text)

data = pd.DataFrame(dict(reference=references, transcription=transcriptions, translation=translations))
data.head()

indexa = 0
audio, text = dataset[indexa]
print(f"Reference: {text}")
print(f"Transcription: {data.iloc[indexa].transcription}")
print(f"Translation: {data.iloc[indexa].translation}")

from IPython.display import Audio
Audio(data=audio, rate=16000)

import torchaudio
import tempfile
import gradio as gr

def process_audio(index, beam_size, best_of, temperature):
    audio, text = dataset[index]

    # Save the tensor to an audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
        temp_filepath = tmpfile.name
        torchaudio.save(temp_filepath, audio.unsqueeze(0), 16000)  # Adjust the sample rate as needed

    # Use the user-provided beam_size and best_of for transcription and translation
    options = dict(language=language, beam_size=beam_size, best_of=best_of, temperature=temperature)
    transcribe_options = dict(task="transcribe", **options)
    translate_options = dict(task="translate", **options)

    transcription = model.transcribe(audio, **transcribe_options)["text"]
    translation = model.transcribe(audio, **translate_options)["text"]

    return text, transcription, translation, temp_filepath

def gradio_interface(index, beam_size, best_of, temperature):
    reference, transcription, translation, temp_filepath = process_audio(index, beam_size, best_of, temperature)

    # Display the results using the file path
    return reference, transcription, translation, gr.Audio(temp_filepath)

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Slider(minimum=0, maximum=len(dataset)-1, step=1, label="Select Audio Sample"),
        gr.Slider(minimum=0, maximum=5, step=1, label="Beam Size", value=5),
        gr.Slider(minimum=0, maximum=5, step=1, label="Best Of", value=5),
        gr.Slider(minimum=0, maximum=1, step=.1, label="Temperature", value=0.2)
    ],
    outputs=[
        gr.Textbox(label="Reference Text"),
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Translation"),
        gr.Audio(label="Audio")
    ],
    title="Learn OpenAI Whisper: Audio Processing",
    description="Slide to select an audio sample and adjust 'beam size', 'best of', and 'temperature' to view its reference text, transcription, and translation along with an audio player."
)

# Launch the app
iface.launch(debug=False)

"""# Word-level timestamps using attention weights

This section demonstrates an advanced technique for extracting word-level timestamps from audio transcriptions using OpenAI's Whisper model, leveraging cross-attention weights. It's designed for readers who are interested in deep learning, speech processing, and specifically those working with the Whisper model for speech-to-text tasks.

### Requirements and Dependencies:
- **Python Libraries:** The script requires `dtw-python` for dynamic time warping, `matplotlib` for visualization, and `pandas` for data handling, among others.
- **Whisper Model:** Understanding the inner workings of OpenAI's Whisper model is crucial, as the script directly interacts with its layers and functions.

### Purpose:
- **Word-Level Timestamps Extraction:** The primary goal is to align the words in the transcript with specific times in the audio recording. This is particularly useful for applications like subtitle generation, detailed audio analysis, and improving accessibility features in media.
- **Granular Analysis with Attention Weights:** It utilizes the model's cross-attention weights to achieve a finer granularity in alignment, beyond what is typically available through simpler transcription methods.

### How It Works:
1. **Dynamic Time Warping (DTW):** The code uses DTW, a well-known algorithm in speech recognition, to find the optimal alignment between two sequences (here, the audio and the text). DTW is particularly effective in compensating for speed variations in speech.
2. **Attention Weights:** By tapping into the cross-attention layers of the Whisper model, the script calculates how each word in the transcript correlates with segments of the audio, providing a basis for timestamping.
3. **Data Preparation and Processing:** It includes preprocessing steps like median filtering to smooth the attention weights and normalization to ensure meaningful comparisons.
4. **Visualization and Output:** The script visualizes the alignment and provides detailed timestamps for each word, making it easy to see how the text matches the audio. It also demonstrates how to handle languages with different characteristics (e.g., space usage in text) for accurate word splitting.

### Applicability:
- **Educational Content:** Readers of "Learn OpenAI Whisper" can use this as a practical example of applying Whisper for detailed speech analysis, going beyond basic transcription to understand the dynamics of attention mechanisms in audio processing.
- **Research and Development:** This approach can inspire researchers and developers to explore advanced speech processing techniques, such as improving automatic subtitle generation, enhancing language learning tools, or creating more interactive and accessible media content.
- **Language-Specific Handling:** The code is designed to accommodate languages with different characteristics, providing insights into handling multilingual audio data effectively.

### Installing Necessary Libraries
First, we install `dtw-python` to use Dynamic Time Warping (DTW) for aligning audio and text sequences based on their temporal similarities.
"""

! pip install dtw-python

"""### Importing Libraries and Setting Up Environment
We import necessary Python libraries for data manipulation, visualization, and handling audio files. This includes `matplotlib` for plotting, `dtw` for dynamic time warping, and Whisper's tokenizer for processing text.

"""

# Commented out IPython magic to ensure Python compatibility.
import string
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker

from IPython.display import display, HTML
from whisper.tokenizer import get_tokenizer
from dtw import dtw
from scipy.ndimage import median_filter

# %matplotlib inline
# %config InlineBackend.figure_format = "retina"

"""### Constants and Configuration
Here, we define constants related to audio processing in Whisper and set up the matplotlib environment for better visual output. This includes setting the audio sample rate and configuring the inline backend for high-resolution figures.

"""

AUDIO_SAMPLES_PER_TOKEN = whisper.audio.HOP_LENGTH * 2
AUDIO_TIME_PER_TOKEN = AUDIO_SAMPLES_PER_TOKEN / whisper.audio.SAMPLE_RATE

medfilt_width = 7
qk_scale = 1.0

tokenizer = get_tokenizer(model.is_multilingual, language=languages[lang])

"""### Handling Fonts for Visualization
This section deals with downloading and setting up fonts compatible with various languages for visualization purposes. It ensures that the plotted figures can correctly display characters from different language scripts.
"""

# This part downloads a repackaged version of the Noto Sans font (either CJK or non-CJK)
# to render various languages in Matplotlib figures.

if languages[lang] in {"Chinese", "Japanese", "Korean"}:
    font = "GoNotoCJKCore.ttf"
else:
    font = "GoNotoCurrent.ttf"

font_release = "https://github.com/satbyy/go-noto-universal/releases/download/v5.2"
if not os.path.exists(font):
    download(f"{font_release}/{font}", font)

prop = fm.FontProperties(fname=font)
props = {'fontproperties': prop}

"""### Preparing for Text Processing
We initialize the tokenizer from Whisper, adjusting for multilingual support and specific language requirements. This is crucial for accurately converting text sequences into tokens that Whisper can process.
#### Utility Functions for Token Splitting
Two utility functions are defined to split tokens based on unicode characters and spaces. These functions help in identifying word boundaries in the transcribed text, which is essential for generating word-level timestamps later.
"""

def split_tokens_on_unicode(tokens: torch.Tensor):
    words = []
    word_tokens = []
    current_tokens = []

    for token in tokens.tolist():
        current_tokens.append(token)
        decoded = tokenizer.decode_with_timestamps(current_tokens)
        if "\ufffd" not in decoded:
            words.append(decoded)
            word_tokens.append(current_tokens)
            current_tokens = []

    return words, word_tokens

def split_tokens_on_spaces(tokens: torch.Tensor):
    subwords, subword_tokens_list = split_tokens_on_unicode(tokens)
    words = []
    word_tokens = []

    for subword, subword_tokens in zip(subwords, subword_tokens_list):
        special = subword_tokens[0] >= tokenizer.eot
        with_space = subword.startswith(" ")
        punctuation = subword.strip() in string.punctuation
        if special or with_space or punctuation:
            words.append(subword)
            word_tokens.append(subword_tokens)
        else:
            words[-1] = words[-1] + subword
            word_tokens[-1].extend(subword_tokens)

    return words, word_tokens

if languages[lang] in {"Chinese", "Japanese", "Thai", "Lao", "Myanmar"}:
    # These languages don't typically use spaces, so it is difficult to split words
    # without morpheme analysis. Here, we instead split words at any
    # position where the tokens are decoded as valid unicode points
    split_tokens = split_tokens_on_unicode
else:
    split_tokens = split_tokens_on_spaces

"""### Setting Up Hooks for Attention Weights
Hooks are installed on the cross-attention layers of the Whisper model to capture the attention weights during inference. These weights are crucial for understanding how the model aligns audio segments with specific words.

"""

# install hooks on the cross attention layers to retrieve the attention weights
QKs = [None] * model.dims.n_text_layer

for i, block in enumerate(model.decoder.blocks):
    block.cross_attn.register_forward_hook(
        lambda _, ins, outs, index=i: QKs.__setitem__(index, outs[-1])
    )

"""### Processing Audio and Generating Timestamps

For a subset of the dataset, this loop processes each audio file, generates its mel spectrogram, and performs inference using the Whisper model. It then uses the captured attention weights and DTW to align words in the transcription with their corresponding audio segments, creating word-level timestamps.

"""

# for the first 10 examples in the dataset
for (audio, label), transcription in zip(dataset, transcriptions[:10]):
    print(transcription)

    duration = len(audio)
    # audio = audio.view(-1)
    mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio)).cuda()
    tokens = torch.tensor(
        [
            *tokenizer.sot_sequence,
            tokenizer.timestamp_begin,
        ] + tokenizer.encode(transcription) + [
            tokenizer.timestamp_begin + duration // AUDIO_SAMPLES_PER_TOKEN,
            tokenizer.eot,
        ]
    ).cuda()
    with torch.no_grad():
        logits = model(mel.unsqueeze(0), tokens.unsqueeze(0))

    weights = torch.cat(QKs)  # layers * heads * tokens * frames
    weights = weights[:, :, :, : duration // AUDIO_SAMPLES_PER_TOKEN].cpu()
    weights = median_filter(weights, (1, 1, 1, medfilt_width))
    weights = torch.tensor(weights * qk_scale).softmax(dim=-1)

    w = weights / weights.norm(dim=-2, keepdim=True)
    matrix = w[-6:].mean(axis=(0, 1))

    alignment = dtw(-matrix.double().numpy())

    jumps = np.pad(np.diff(alignment.index1s), (1, 0), constant_values=1).astype(bool)
    jump_times = alignment.index2s[jumps] * AUDIO_TIME_PER_TOKEN
    words, word_tokens = split_tokens(tokens)

    '''
    Visualizing Alignment and Attention Weights
    This part visualizes the alignment between audio and text using the calculated attention weights.
    It plots the cross-attention matrix and overlays the DTW path, showing how each word aligns with segments of the audio.
    '''
    plt.figure(figsize=(8, 8))
    plt.imshow(matrix, aspect="auto")
    plt.plot(alignment.index2s, alignment.index1s, color="red")

    xticks = np.arange(0, matrix.shape[1], 1 / AUDIO_TIME_PER_TOKEN)
    xticklabels = (xticks * AUDIO_TIME_PER_TOKEN).round().astype(np.int32)
    plt.xticks(xticks, xticklabels)
    plt.xlabel("Time (s)")

    # display tokens and words as tick labels
    ylims = plt.gca().get_ylim()

    ax = plt.gca()
    ax.tick_params('both', length=0, width=0, which='minor', pad=6)

    ax.yaxis.set_ticks_position("left")
    ax.yaxis.set_label_position("left")
    ax.invert_yaxis()
    ax.set_ylim(ylims)

    major_ticks = [-0.5]
    minor_ticks = []
    current_y = 0

    for word, word_token in zip(words, word_tokens):
        minor_ticks.append(current_y + len(word_token) / 2 - 0.5)
        current_y += len(word_token)
        major_ticks.append(current_y - 0.5)

    ax.yaxis.set_minor_locator(ticker.FixedLocator(minor_ticks))
    ax.yaxis.set_minor_formatter(ticker.FixedFormatter(words))
    ax.set_yticks(major_ticks)
    ax.yaxis.set_major_formatter(ticker.NullFormatter())

    for label in ax.get_yminorticklabels():
        label.set_fontproperties(prop)

    plt.ylabel("Words")
    plt.show()

    '''
    Generating Word-Level Timestamps
    Finally, the code calculates and displays the start and end times for each word in the transcription.
    This allows for a granular analysis of the speech, which can be used for detailed subtitles, speech analysis, and more interactive applications.
    '''
    word_boundaries = np.pad(np.cumsum([len(t) for t in word_tokens[:-1]]), (1, 0))
    begin_times = jump_times[word_boundaries[:-1]]
    end_times = jump_times[word_boundaries[1:]]

    data = [
        dict(word=word, begin=begin, end=end)
        for word, begin, end in zip(words[:-1], begin_times, end_times)
        if not word.startswith("<|") and word.strip() not in ".,!?、。"
    ]

    display(pd.DataFrame(data))
    display(HTML("<hr>"))