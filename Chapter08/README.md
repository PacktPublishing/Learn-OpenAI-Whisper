# Learn OpenAI Whisper - Chapter 8

## Diarizing speech with WhisperX and NVIDIA's NeMo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1-TSAhmGl5QplD9-NzWLOONkH43SEMwdF)

This notebook offers a step-by-step guide to implementing speaker diarization using [WhisperX](https://replicate.com/dinozoiddev/whisperx) and NVIDIA's NeMo. WhisperX combines the power of `whisper-large-v3` with diarization upgrades, while NeMo provides a robust framework for speaker diarization. The goal is to demonstrate how these tools can be integrated to accurately identify "who spoke when" in an audio file, enhancing the capabilities of automated speech recognition (ASR) systems.

### Notebook Structure

The notebook is organized into key sections, each addressing a specific aspect of the diarization process:

1. **Setting up the environment**: Installs necessary dependencies, including Whisper, NeMo, and supporting libraries.

2. **Streamlining the diarization workflow with helper functions**: Utility functions for audio manipulation, data processing, and speaker embedding generation.

3. **Separating music from speech using Demucs**: Separates music from speech using Demucs and convert audio to mono format for NeMo compatibility.

4. **Transcribing audio using WhisperX**: Transcribes audio using WhisperX, leveraging its high accuracy in speech recognition.

5. **Aligning Transcriptions with Wav2Vec2**: Aligns the transcription with the original audio using Wav2Vec2, a neural network designed for speech recognition and alignment tasks.

6. **Using NeMo's MSDD model for speaker diarization**: Employs NVIDIA's NeMo MSDD model to separate transcribed audio into segments based on speaker identity.

7. **Mapping speakers to sentences according to timestamps**: Maps identified speakers to corresponding sentences in the transcription based on timestamps.

8. **Enhancing speaker attribution with punctuation-based realignment**: Refines speaker labels using punctuation, addressing scenarios where sentences are split between speakers or background comments occur.

9. **Finalizing the diarization process**: Cleanup, result export, and speaker name mapping.

This notebook provides a comprehensive resource for researchers, developers, and practitioners interested in exploring advanced diarization techniques within ASR systems. Integrating Whisper's transcription capabilities with NeMo's diarization framework offers a powerful solution for analyzing speech in audio recordings.
