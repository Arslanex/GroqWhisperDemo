"""
Utility functions for Groq Transcribe module.

Provides helper functions for audio transcription, 
including export, language detection, and file validation.
"""

import os
import json
import soundfile as sf
import wave
import mutagen
from typing import Dict, Union, Optional, List

def export_transcription(
    transcription: Dict, 
    output_format: str = 'json', 
    output_path: Optional[str] = None
) -> str:
    """
    Export transcription to various formats.
    
    :param transcription: Transcription result dictionary
    :param output_format: Output format (json, srt, vtt)
    :param output_path: Path to save the exported file
    :return: Exported transcription content
    """
    # Existing export logic
    if output_format == 'json':
        content = json.dumps(transcription, indent=2)
    elif output_format == 'text':
        content = transcription.get('text', '')
    else:
        raise ValueError(f"Unsupported export format: {output_format}")
    
    # Save to file if output path provided
    if output_path:
        with open(output_path, 'w') as f:
            f.write(content)
    
    return content

def detect_language(transcription: Dict) -> str:
    """
    Detect language from transcription result.
    
    :param transcription: Transcription result dictionary
    :return: Detected language code
    """
    return transcription.get('language', 'unknown')

def validate_audio_file(
    audio_path: str, 
    max_file_size_mb: float = 25,
    min_file_length_seconds: float = 0.01,
    supported_extensions: List[str] = None
) -> Dict[str, Union[float, int, str]]:
    """
    Validate audio file with multiple detection methods.
    
    :param audio_path: Path to the audio file
    :param max_file_size_mb: Maximum allowed file size in MB
    :param min_file_length_seconds: Minimum allowed audio length
    :param supported_extensions: List of supported file extensions
    :return: Dictionary with audio file details
    """
    # Default supported extensions if not provided
    if supported_extensions is None:
        supported_extensions = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    
    # Check file existence
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Validate file extension
    file_ext = os.path.splitext(audio_path)[1].lower()
    if file_ext not in supported_extensions:
        raise ValueError(
            f"Unsupported file type: {file_ext}. "
            f"Supported types: {', '.join(supported_extensions)}"
        )
    
    # Check file size
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    if file_size_mb > max_file_size_mb:
        raise ValueError(
            f"Audio file exceeds {max_file_size_mb} MB limit. "
            f"Current size: {file_size_mb:.2f} MB"
        )
    
    # Try multiple methods to get audio details
    audio_details = {
        'duration': 0,
        'channels': 1,
        'sample_rate': 0,
        'file_size_mb': file_size_mb
    }
    
    # Method 1: soundfile
    try:
        with sf.SoundFile(audio_path) as audio_file:
            audio_details['duration'] = len(audio_file) / audio_file.samplerate
            audio_details['channels'] = audio_file.channels
            audio_details['sample_rate'] = audio_file.samplerate
            return audio_details
    except Exception as sf_error:
        print(f"Soundfile method failed: {sf_error}")
    
    # Method 2: mutagen
    try:
        audio_file = mutagen.File(audio_path)
        if hasattr(audio_file, 'info'):
            audio_details['duration'] = audio_file.info.length
            audio_details['channels'] = getattr(audio_file.info, 'channels', 1)
            audio_details['sample_rate'] = getattr(audio_file.info, 'sample_rate', 0)
            return audio_details
    except Exception as mutagen_error:
        print(f"Mutagen method failed: {mutagen_error}")
    
    # Method 3: wave module (for WAV files)
    if file_ext == '.wav':
        try:
            with wave.open(audio_path, 'rb') as wav_file:
                audio_details['channels'] = wav_file.getnchannels()
                audio_details['sample_rate'] = wav_file.getframerate()
                audio_details['duration'] = wav_file.getnframes() / wav_file.getframerate()
            return audio_details
        except Exception as wave_error:
            print(f"Wave method failed: {wave_error}")
    
    # Validate minimum file length
    if audio_details['duration'] < min_file_length_seconds:
        raise ValueError(
            f"Audio file too short. Minimum length is {min_file_length_seconds} seconds. "
            f"Current length: {audio_details['duration']:.2f} seconds"
        )
    
    # Fallback: use os.path for basic info
    return audio_details
