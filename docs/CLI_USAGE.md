# Groq Transcribe: Command-Line Interface (CLI) Usage

## Installation

```bash
pip install groq-transcribe
```

## Basic Usage

### Transcribe a Single Audio File

```bash
# Basic transcription
groq-transcribe audio.mp3

# Specify output file
groq-transcribe audio.mp3 -o transcript.json

# Choose response format
groq-transcribe audio.mp3 -f verbose_json
```

## Advanced CLI Options

```bash
# Full CLI command syntax
groq-transcribe [OPTIONS] AUDIO_FILE

Options:
  -o, --output FILE        Output file path
  -f, --format FORMAT      Response format (json, verbose_json, text)
  -m, --model MODEL        Whisper model to use
  -l, --language LANG      Language hint for transcription
  --help                   Show help message
```

## Examples

```bash
# Transcribe with specific model
groq-transcribe audio.mp3 -m whisper-large-v3-turbo

# Specify language
groq-transcribe audio.mp3 -l en

# Batch transcription
groq-transcribe audio1.mp3 audio2.wav audio3.mp4 -o transcripts/

# Export in different formats
groq-transcribe audio.mp3 -f json -o transcript.json
groq-transcribe audio.mp3 -f text -o transcript.txt
```

## Configuration

### API Key

Set your Groq API key using environment variables:

```bash
# Option 1: Export in shell
export GROQ_API_KEY=your_api_key_here

# Option 2: Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## Troubleshooting

- Ensure you have a valid Groq API key
- Check audio file format and size
- Verify network connectivity
- Use `--help` for detailed command information
