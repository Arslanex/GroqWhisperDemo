"""
Command-line interface for Groq Transcribe.

Provides a CLI tool for transcribing audio files using the Groq Cloud API.
"""

import os
import sys
import click
from typing import List, Optional
from dotenv import load_dotenv

# Import local modules
from .transcriber import GroqTranscriber
from .utils import export_transcription, detect_language, validate_audio_file

# Load environment variables
load_dotenv()

@click.command()
@click.argument('audio_files', nargs=-1, type=click.Path(exists=True))
@click.option('-o', '--output', 'output_path', 
              help='Output file or directory for transcription results.')
@click.option('-f', '--format', 'response_format', 
              type=click.Choice(['json', 'verbose_json', 'text'], case_sensitive=False), 
              default='verbose_json', 
              help='Response format for transcription.')
@click.option('-m', '--model', 'model', 
              type=click.Choice(GroqTranscriber.SUPPORTED_MODELS), 
              default='whisper-large-v3', 
              help='Whisper model to use for transcription.')
@click.option('-l', '--language', 'language', 
              help='Optional language hint for transcription.')
@click.option('--validate-only', 'validate_only', 
              is_flag=True, 
              help='Only validate audio files without transcribing.')
def transcribe_cli(
    audio_files: List[str], 
    output_path: Optional[str] = None, 
    response_format: str = 'verbose_json',
    model: str = 'whisper-large-v3',
    language: Optional[str] = None,
    validate_only: bool = False
) -> None:
    """
    Transcribe audio files using Groq Cloud API.
    
    Supports batch transcription with various output options.
    """
    # Validate API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        click.echo("Error: GROQ_API_KEY not found. Set it in .env or as an environment variable.", err=True)
        sys.exit(1)

    # Validate input
    if not audio_files:
        click.echo("Error: No audio files provided.", err=True)
        sys.exit(1)

    # Prepare output directory
    if output_path and len(audio_files) > 1:
        os.makedirs(output_path, exist_ok=True)

    # Initialize transcriber
    try:
        transcriber = GroqTranscriber(
            api_key=api_key, 
            model=model
        )
    except ValueError as e:
        click.echo(f"Error initializing transcriber: {e}", err=True)
        sys.exit(1)

    # Process each audio file
    for audio_file in audio_files:
        try:
            # Validate audio file
            audio_details = validate_audio_file(audio_file)
            click.echo(f"Audio File Details for {os.path.basename(audio_file)}:")
            click.echo(f"  Duration: {audio_details['duration']:.2f} seconds")
            click.echo(f"  Channels: {audio_details['channels']}")
            click.echo(f"  Sample Rate: {audio_details['sample_rate']} Hz")
            click.echo(f"  File Size: {audio_details['file_size_mb']:.2f} MB")

            # Skip transcription if validate-only flag is set
            if validate_only:
                continue

            # Transcribe audio file
            transcription = transcriber.transcribe(
                audio_file, 
                response_format=response_format,
                language=language
            )

            # Determine output path
            if output_path:
                if os.path.isdir(output_path):
                    base_name = os.path.splitext(os.path.basename(audio_file))[0]
                    output_file = os.path.join(output_path, f"{base_name}_transcript.{response_format}")
                else:
                    output_file = output_path
            else:
                base_name = os.path.splitext(os.path.basename(audio_file))[0]
                output_file = f"{base_name}_transcript.{response_format}"

            # Export transcription
            export_transcription(
                transcription, 
                output_format=response_format, 
                output_path=output_file
            )

            click.echo(f"Transcription saved to {output_file}")

        except Exception as e:
            click.echo(f"Error processing {audio_file}: {e}", err=True)

def main():
    """Entry point for CLI."""
    transcribe_cli()

if __name__ == '__main__':
    main()
