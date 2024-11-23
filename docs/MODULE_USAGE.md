# Groq Transcribe: Module Usage Guide

## Installation

```bash
pip install groq-transcribe
```

## Basic Usage

### Transcribing a Single Audio File

```python
from groq_transcribe import GroqTranscriber

# Initialize the transcriber
transcriber = GroqTranscriber(
    api_key='your_groq_api_key',  # Optional if set in .env
    model='whisper-large-v3'      # Optional, defaults to whisper-large-v3
)

# Transcribe an audio file
transcription = transcriber.transcribe('path/to/audio.mp3')

# Access transcription details
print(transcription['text'])  # Full transcription text
print(transcription['segments'])  # Timestamped segments
```

### Batch Transcription

```python
# Transcribe multiple files
audio_files = ['audio1.mp3', 'audio2.wav', 'audio3.mp4']
batch_transcriptions = transcriber.batch_transcribe(audio_files)

for transcription in batch_transcriptions:
    print(transcription['text'])
```

### Advanced Options

```python
# Specify response format and language
transcription = transcriber.transcribe(
    'path/to/audio.mp3', 
    response_format='verbose_json',  # Options: json, verbose_json, text
    language='en'  # Optional language hint
)

# Export transcription
from groq_transcribe import export_transcription

export_transcription(
    transcription, 
    output_format='json', 
    output_path='transcript.json'
)

# Detect language
from groq_transcribe import detect_language

language = detect_language(transcription)
print(f"Detected Language: {language}")
```

## Error Handling

```python
try:
    transcription = transcriber.transcribe('path/to/audio.mp3')
except ValueError as e:
    print(f"Validation Error: {e}")
except requests.RequestException as e:
    print(f"API Request Error: {e}")
```

## Environment Variables

Create a `.env` file in your project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

This allows you to omit the API key when initializing the transcriber.
