# Groq Whisper Transcription Demo

## Overview
This project provides a robust audio transcription module using the Groq Cloud API and Whisper models. It includes comprehensive audio file validation, error handling, and flexible transcription options.

## Features
- Multiple Whisper model support
- Strict audio file validation
- Detailed error handling
- Command-line interface for easy transcription

## Prerequisites
- Python 3.8+
- Groq Cloud API Key

## Installation
1. Clone the repository
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up your Groq API Key
```bash
# Create a .env file in the project root
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## Usage
### Command Line
```bash
python transcribe.py /path/to/audio/file.mp3
```

### In Python Script
```python
from groq_transcriber import GroqTranscriber

transcriber = GroqTranscriber(model="whisper-large-v3")
result = transcriber.transcribe("audio.mp3")
print(result)
```

## Supported Audio Formats
- MP3
- MP4
- MPEG
- M4A
- WAV
- WebM

## Limitations
- Maximum file size: 25 MB
- Minimum file length: 0.01 seconds
- Minimum billed length: 10 seconds

## Troubleshooting
- Ensure your API key is valid
- Check audio file format and size
- Verify network connectivity

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

## License
[MIT](https://choosealicense.com/licenses/mit/)
