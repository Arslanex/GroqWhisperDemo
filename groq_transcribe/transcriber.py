import os
import requests
from typing import Dict, List, Optional, Union, Any
import json
from dotenv import load_dotenv
import soundfile as sf
import wave
import mutagen

# Load environment variables
load_dotenv()

class GroqTranscriber:
    """
    A comprehensive audio transcription class using Groq Cloud API.
    
    Supports multiple Whisper models, detailed transcription with timestamps,
    and flexible response formats while enforcing strict audio file limitations.
    """
    
    SUPPORTED_MODELS = [
        "whisper-large-v3-turbo", 
        "distil-whisper-large-v3-en", 
        "whisper-large-v3"
    ]
    
    SUPPORTED_FORMATS = ["json", "verbose_json", "text"]
    
    SUPPORTED_EXTENSIONS = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    
    MAX_FILE_SIZE_MB = 25
    MIN_FILE_LENGTH_SECONDS = 0.01
    MIN_BILLED_LENGTH_SECONDS = 10
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: str = "whisper-large-v3",
        base_url: str = "https://api.groq.com/openai/v1/audio/transcriptions"
    ):
        """
        Initialize the Groq Transcriber with API credentials and validation.
        
        :param api_key: Groq Cloud API key. Defaults to GROQ_API_KEY env variable.
        :param model: Whisper model to use. Defaults to whisper-large-v3.
        :param base_url: Groq API endpoint. Defaults to transcription endpoint.
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model. Choose from: {', '.join(self.SUPPORTED_MODELS)}")
        
        self.model = model
        self.base_url = base_url
    
    def _get_audio_details(self, audio_path: str) -> Dict[str, Union[float, int, str]]:
        """
        Extract detailed audio file information using multiple methods.
        
        :param audio_path: Path to the audio file
        :return: Dictionary with audio file details
        """
        # Check file existence
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Validate file extension
        file_ext = os.path.splitext(audio_path)[1].lower()
        if file_ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {file_ext}. "
                f"Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # Check file size
        file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            raise ValueError(
                f"Audio file exceeds {self.MAX_FILE_SIZE_MB} MB limit. "
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
        
        # Fallback: use os.path for basic info
        return audio_details
    
    def _validate_audio_file(self, audio_path: str) -> None:
        """
        Comprehensive validation of audio file before transcription.
        
        :param audio_path: Path to the audio file
        :raises ValueError: If file does not meet Groq API requirements
        """
        # Get audio details
        audio_details = self._get_audio_details(audio_path)
        
        # Debug print for audio file details
        print(f"Audio File Details:")
        print(f"  Duration: {audio_details['duration']:.2f} seconds")
        print(f"  Channels: {audio_details['channels']}")
        print(f"  Sample Rate: {audio_details['sample_rate']} Hz")
        print(f"  File Size: {audio_details['file_size_mb']:.2f} MB")
        
        # Check minimum file length
        if audio_details['duration'] < self.MIN_FILE_LENGTH_SECONDS:
            raise ValueError(
                f"Audio file too short. Minimum length is {self.MIN_FILE_LENGTH_SECONDS} seconds. "
                f"Current length: {audio_details['duration']:.2f} seconds"
            )
        
        # Warn about minimum billed length
        if audio_details['duration'] < self.MIN_BILLED_LENGTH_SECONDS:
            print(
                f"Warning: Audio shorter than {self.MIN_BILLED_LENGTH_SECONDS} seconds. "
                "You will be billed for a full 10 seconds."
            )
        
        # Check for multiple audio tracks
        if audio_details['channels'] > 1:
            print(
                "Warning: Multiple audio tracks detected. "
                "Only the first track will be transcribed."
            )

    def transcribe(
        self, 
        audio_path: str, 
        response_format: str = "verbose_json",
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe an audio file using the Groq Cloud API.
        
        :param audio_path: Path to the audio file to transcribe
        :param response_format: Format of the transcription response
        :param language: Optional language code for transcription
        :return: Transcription result dictionary
        """
        # Validate audio file before transcription
        self._validate_audio_file(audio_path)
        
        # Validate response format
        if response_format not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported response format. Choose from: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        # Prepare API request headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            # Note: Content-Type will be set automatically by requests when using files
        }
        
        # Prepare API request payload
        payload = {
            "model": self.model,
            "response_format": response_format
        }
        
        # Optional language specification
        if language:
            payload["language"] = language
        
        # Prepare files for multipart upload
        files = {
            "file": (os.path.basename(audio_path), open(audio_path, "rb"), "audio/mpeg")
        }
        
        # Debug print for API request details
        print("API Request Details:")
        print(f"  URL: {self.base_url}")
        print(f"  Model: {self.model}")
        print(f"  Response Format: {response_format}")
        print(f"  API Key: {self.api_key[:3]}...{self.api_key[-4:]}")
        
        try:
            # Make the API request
            response = requests.post(
                self.base_url, 
                headers=headers, 
                data=payload,
                files=files
            )
            
            # Check for API errors
            if response.status_code != 200:
                print("API Error Details:")
                print(f"  Status Code: {response.status_code}")
                print(f"  Response Content: {response.text}")
                print(f"  Response Headers: {dict(response.headers)}")
                
                raise ValueError(
                    f"Transcription request failed: {response.status_code} - {response.text}"
                )
            
            # Parse and return the transcription result
            return response.json()
        
        except requests.RequestException as e:
            print(f"Request error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            raise
        finally:
            # Ensure file is closed
            files["file"][1].close()

    def batch_transcribe(
        self, 
        audio_paths: List[str], 
        response_format: str = "verbose_json"
    ) -> List[Dict[str, Any]]:
        """
        Transcribe multiple audio files in sequence.
        
        :param audio_paths: List of paths to audio files
        :param response_format: Format of the response
        :return: List of transcription results
        """
        return [self.transcribe(path, response_format) for path in audio_paths]
