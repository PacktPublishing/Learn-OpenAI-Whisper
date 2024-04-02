# Learn OpenAI Whisper
Learn OpenAI Whisper, published by Packt

This repository contains the code, examples, and resources for the book "Learn OpenAI Whisper" by Josué R. Batista, published by Packt.

## About the Book

"Learn OpenAI Whisper" is a comprehensive guide that aims to transform your understanding of generative AI through robust and accurate speech processing solutions. The book delves into the profound applications and intricate architecture of OpenAI's Whisper, making it an indispensable resource for intermediate to advanced readers.

## About the Author

Josué R. Batista is a Digital Transformation Strategist at Harvard Business School, supporting the industrialization of generative AI and large language models (LLMs), promoting innovative learning experiences for a global audience. With an MBA, a Masters of Science in Information Systems Management, and extensive experience in AI/ML transformation, Josué is well-equipped to guide readers through the complex world of OpenAI's Whisper.

## Book and Repository Structure
| Chapter | Title                                           | Description                                                                                                                                                                                                                                                                         |
|---------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1       | Unveiling Whisper - Introducing OpenAI's Whisper | This chapter serves as an entry point into the world of OpenAI's Whisper technology. It outlines the key features and capabilities of Whisper, helping readers grasp its core functionalities. It also provides hands-on guidance for initial setup and basic usage examples.<br><br>Notebooks:<br>- [LOAIW_ch01_using_Whisper_in_Google_Colab.ipynb](/Chapter01/LOAIW_ch01_using_Whisper_in_Google_Colab.ipynb)               |
| 2       | Underlying Architecture                          | This chapter delves into the nuts and bolts of Whisper's ASR system. It explains the system's critical components and functions, shedding light on how the technology interprets and processes human speech. It also explores best practices for performance optimization.<br><br>Notebooks:<br>- [LOAIW_ch02_exploring_audio_data_workflows.ipynb](/Chapter02/LOAIW_ch02_exploring_audio_data_workflows.ipynb)                |
| 3       | Diving into the Architecture                     | Chapter 3 provides a comprehensive understanding of the transformer model, which is the backbone of OpenAI's Whisper. Readers will explore the architectural intricacies of Whisper, including the encoder-decoder mechanics, and learn how the transformer model drives effective speech recognition.<br><br>Notebooks:<br>- [LOAIW_ch03_working_with_audio_data_via_Hugging_Face.ipynb](/Chapter03/LOAIW_ch03_working_with_audio_data_via_Hugging_Face.ipynb) |
| 4       | Customizing and Optimizing for Efficiency        | In this chapter, readers will embark on a hands-on journey to fine-tune OpenAI's Whisper model for specific domain and language needs. They will learn to set up a robust Python environment, integrate diverse datasets, and tailor Whisper's predictions to align with target applications.<br><br>Notebooks:<br>- [LOAIW_ch04_fine_tune_whisper_with_Hugging_Face_transformers.ipynb](/Chapter04/LOAIW_ch04_fine_tune_whisper_with_Hugging_Face_transformers.ipynb) |
| 5       | Applying Whisper in Various Contexts             | Chapter 5 explores the remarkable capabilities of OpenAI's Whisper in transforming spoken language into written text across various applications, including transcription services, voice assistants, chatbots, and accessibility features.<br><br>Notebooks:<br>- [LOAIW_ch05_1_setting_up_Whisper_for_transcription.ipynb](/Chapter05/LOAIW_ch05_1_setting_up_Whisper_for_transcription.ipynb)<br>- [LOAIW_ch05_2_transcription_and_translation_with_Whisper.ipynb](/Chapter05/LOAIW_ch05_2_transcription_and_translation_with_Whisper.ipynb)<br>- [LOAIW_ch05_3_Whisper_and_Stable_LM_Zephyr_3B_voice_assistant_GPU.ipynb](/Chapter05/LOAIW_ch05_3_Whisper_and_Stable_LM_Zephyr_3B_voice_assistant_GPU.ipynb)<br>- [LOAIW_ch05_4_Whisper_img2txt_Llava_image_assistant.ipynb](/Chapter05/LOAIW_ch05_4_Whisper_img2txt_Llava_image_assistant.ipynb)                                                |
| 6       | Expanding Applications with Whisper              | This chapter explores expanding the applications of OpenAI's Whisper for tasks such as precise multilingual transcription, indexing content for enhanced discoverability, and utilizing transcription for SEO and content marketing. It also covers integrating Whisper with customer service and language learning platforms.<br><br>Notebooks:<br>- [LOAIW_ch06_1_Transcripting_translating_YouTube_with_Whisper.ipynb](/Chapter06/LOAIW_ch06_1_Transcripting_translating_YouTube_with_Whisper.ipynb)<br>- [LOAIW_ch06_2_Transcripting_translating_RSS_with_Whisper.ipynb](/Chapter06/LOAIW_ch06_2_Transcripting_translating_RSS_with_Whisper.ipynb)<br>- [LOAIW_ch06_3_Creating_YouTube_subtitles_with_Whisper_and_OpenVINO.ipynb](/Chapter06/LOAIW_ch06_3_Creating_YouTube_subtitles_with_Whisper_and_OpenVINO.ipynb) |
| 7       | Exploring Advanced Voice Capabilities            | Chapter 7 explores the advanced voice capabilities of OpenAI's Whisper, focusing on techniques that enhance its performance, such as quantization, and its potential for speaker diarization and real-time speech recognition.<br><br>Notebooks:<br>- [LOAIW_ch07_1_quantizing_Whisper_with_CTranslate2.ipynb](/Chapter07/LOAIW_ch07_1_quantizing_Whisper_with_CTranslate2.ipynb)<br>- [LOAIW_ch07_2_Quantizing_Distil_Whisper_with_OpenVINO.ipynb](/Chapter07/LOAIW_ch07_2_Quantizing_Distil_Whisper_with_OpenVINO.ipynb)                                                           |
| 8       | Exploring Advanced Voice Capabilities            | This chapter explores how to harness OpenAI's Whisper for voice cloning, allowing readers to create personalized voice models that capture the unique characteristics of a target speaker. It covers the fundamentals of text-to-speech in voice cloning, converting audio files to the LJSpeech format, fine-tuning voice cloning models using the DLAS toolkit, and synthesizing realistic speech using the fine-tuned voice model.<br><br>Notebooks:<br>- [LOAIW_ch08_1_Cloning_voices_with_tortoise_tts_fast.ipynb](/Chapter08/LOAIW_ch08_1_Cloning_voices_with_tortoise_tts_fast.ipynb)<br>- [LOAIW_ch08_2_Processing_audio_to_LJ_format_with_Whisper_OZEN.ipynb](/Chapter08/LOAIW_ch08_2_Processing_audio_to_LJ_format_with_Whisper_OZEN.ipynb)<br>- [LOAIW_ch08_3_Fine_tuning_voice_cloning_with_DLAS.ipynb](/Chapter08/LOAIW_ch08_3_Fine_tuning_voice_cloning_with_DLAS.ipynb)<br>- [LOAIW_ch08_4_Synthetizing_speech_using_a_fine_tuned_voice_model.ipynb](/Chapter08/LOAIW_ch08_4_Synthetizing_speech_using_a_fine_tuned_voice_model.ipynb)                                                         |
| 9       | Shaping the Future with Whisper                  | The final chapter provides a forward-looking perspective on the evolving field of Automatic Speech Recognition (ASR) and Whisper's role. It delves into upcoming trends, anticipated features, and the general direction that voice technologies are taking.                               |

## Getting Started

To get started with the code examples, navigate to the desired chapter directory and run the Jupyter notebooks

## Resources

- [OpenAI Whisper Documentation](https://openai.com/blog/whisper/)
- [Packt Publishing](https://www.packtpub.com/)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you run into issues with the notebooks, please create an issue with details, I am also available here in GitHub @josuebatista and [LinkedIn](https://http://www.linkedin.com/in/josuebatista)
