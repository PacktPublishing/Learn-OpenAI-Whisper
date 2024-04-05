# Learn OpenAI Whisper - Chapter 1
## Using Whisper in Google Colab
This notebook provides a simple template for using OpenAI's Whisper for audio transcription in Google Colab.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uka0UhZJBWIwLcubsFbiOw8fNGlBBI-a)
## Install Whisper
Run the cell below to install Whisper.

The Python libraries `openai`, `cohere`, and `tiktoken` are also installed because of dependencies for the `llmx` library. That is because `llmx` relies on them to function correctly. Each of these libraries provides specific functionalities that `llmx` uses.

1. `openai`: This is the official Python library for the OpenAI API. It provides convenient access to the OpenAI REST API from any Python 3.7+ application. The library includes type definitions for all request parameters and response fields, and offers both synchronous and asynchronous clients powered by `httpx`.

2. `cohere`: The Cohere platform builds natural language processing and generation into your product with a few lines of code. It can solve a broad spectrum of natural language use cases, including classification, semantic search, paraphrasing, summarization, and content generation.

3. `tiktoken`: This is a fast Byte Pair Encoding (BPE) tokenizer for use with OpenAI's models. It's used to tokenize text into subwords, a necessary step before feeding text into many modern language models.
