"""
Groq Transcribe: A comprehensive audio transcription module.

This module provides tools for transcribing audio files using the Groq Cloud API
with advanced features like multi-method audio file validation, 
flexible response formats, and batch transcription support.
"""

from .transcriber import GroqTranscriber
from .cli import transcribe_cli, main
from .utils import (
    export_transcription, 
    detect_language, 
    validate_audio_file
)

__all__ = [
    'GroqTranscriber',
    'transcribe_cli',
    'main',
    'export_transcription',
    'detect_language',
    'validate_audio_file'
]

__version__ = '0.1.0'
