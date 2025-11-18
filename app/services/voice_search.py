"""
Voice Search Service
Handles voice-to-text conversion for hands-free stock search queries
"""

import io
import logging
from typing import Dict, Optional, Tuple
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

logger = logging.getLogger(__name__)


class VoiceSearchService:
    """
    Service for converting voice queries to text
    Supports multiple languages and audio formats
    """

    # Supported languages (ISO 639-1 codes)
    SUPPORTED_LANGUAGES = {
        "en": "en-US",  # English (US)
        "en-gb": "en-GB",  # English (UK)
        "es": "es-ES",  # Spanish
        "fr": "fr-FR",  # French
        "de": "de-DE",  # German
        "it": "it-IT",  # Italian
        "pt": "pt-BR",  # Portuguese (Brazil)
        "ja": "ja-JP",  # Japanese
        "ko": "ko-KR",  # Korean
        "zh": "zh-CN",  # Chinese (Simplified)
    }

    # Audio format conversions
    SUPPORTED_FORMATS = ["wav", "mp3", "ogg", "flac", "m4a", "webm"]

    def __init__(self):
        """Initialize the voice search service"""
        self.recognizer = sr.Recognizer()

        # Configure recognizer settings for better accuracy
        self.recognizer.energy_threshold = 300  # Minimum audio energy to consider for recording
        self.recognizer.dynamic_energy_threshold = True  # Automatically adjust for ambient noise
        self.recognizer.pause_threshold = 0.8  # Seconds of non-speaking audio before phrase is complete

    async def transcribe_audio(
        self,
        audio_data: bytes,
        audio_format: str = "wav",
        language: str = "en",
        use_google: bool = True,
        alternative_count: int = 1
    ) -> Dict[str, any]:
        """
        Transcribe audio to text

        Args:
            audio_data: Raw audio bytes
            audio_format: Audio format (wav, mp3, ogg, etc.)
            language: Language code (en, es, fr, etc.)
            use_google: Use Google Speech Recognition (free, no API key needed)
            alternative_count: Number of alternative transcriptions to return

        Returns:
            Dictionary with transcription results:
            {
                "text": str,  # Primary transcription
                "alternatives": List[str],  # Alternative transcriptions
                "confidence": float,  # Confidence score (0-1)
                "language": str,  # Detected/used language
                "duration": float  # Audio duration in seconds
            }
        """
        try:
            # Convert to WAV if needed
            audio_wav = await self._convert_to_wav(audio_data, audio_format)

            # Create AudioData object from WAV
            with sr.AudioFile(audio_wav) as source:
                # Record the audio data
                audio = self.recognizer.record(source)

                # Get audio duration
                duration = len(audio.frame_data) / audio.sample_rate / audio.sample_width

            # Get language code
            lang_code = self.SUPPORTED_LANGUAGES.get(language.lower(), "en-US")

            # Transcribe using selected engine
            if use_google:
                result = await self._transcribe_google(audio, lang_code, alternative_count)
            else:
                # Fallback to Google if no other engine specified
                result = await self._transcribe_google(audio, lang_code, alternative_count)

            result["duration"] = duration
            result["language"] = language

            logger.info(f"Transcribed audio: '{result['text'][:50]}...' "
                       f"(confidence: {result['confidence']:.2f})")

            return result

        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise ValueError(f"Failed to transcribe audio: {str(e)}")

    async def _convert_to_wav(self, audio_data: bytes, source_format: str) -> io.BytesIO:
        """
        Convert audio to WAV format for speech recognition

        Args:
            audio_data: Raw audio bytes
            source_format: Source audio format

        Returns:
            BytesIO object containing WAV audio
        """
        if source_format.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported audio format: {source_format}. "
                           f"Supported: {', '.join(self.SUPPORTED_FORMATS)}")

        # If already WAV, return as-is
        if source_format.lower() == "wav":
            return io.BytesIO(audio_data)

        try:
            # Create temporary file for conversion
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{source_format}"
            ) as temp_input:
                temp_input.write(audio_data)
                temp_input_path = temp_input.name

            # Load audio with pydub
            audio = AudioSegment.from_file(temp_input_path, format=source_format)

            # Convert to WAV
            wav_io = io.BytesIO()
            audio.export(
                wav_io,
                format="wav",
                parameters=["-ac", "1", "-ar", "16000"]  # Mono, 16kHz for speech recognition
            )
            wav_io.seek(0)

            # Clean up temp file
            os.unlink(temp_input_path)

            logger.info(f"Converted {source_format} to WAV for transcription")

            return wav_io

        except Exception as e:
            logger.error(f"Error converting audio format: {str(e)}")
            raise ValueError(f"Failed to convert audio from {source_format} to WAV: {str(e)}")

    async def _transcribe_google(
        self,
        audio: sr.AudioData,
        language: str,
        alternative_count: int = 1
    ) -> Dict[str, any]:
        """
        Transcribe using Google Speech Recognition

        Args:
            audio: AudioData object
            language: Language code
            alternative_count: Number of alternatives to return

        Returns:
            Dictionary with transcription results
        """
        try:
            # Try with show_all to get confidence and alternatives
            response = self.recognizer.recognize_google(
                audio,
                language=language,
                show_all=True
            )

            if not response:
                raise ValueError("No transcription results")

            # Extract results
            if isinstance(response, dict) and "alternative" in response:
                alternatives = response["alternative"]

                # Primary result
                primary = alternatives[0]
                text = primary.get("transcript", "")
                confidence = primary.get("confidence", 0.0)

                # Alternative transcriptions
                alt_texts = [
                    alt.get("transcript", "")
                    for alt in alternatives[1:alternative_count]
                ]

                return {
                    "text": text,
                    "alternatives": alt_texts,
                    "confidence": confidence,
                }
            else:
                # Fallback for simple response
                text = str(response) if response else ""
                return {
                    "text": text,
                    "alternatives": [],
                    "confidence": 0.8,  # Default confidence
                }

        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
            return {
                "text": "",
                "alternatives": [],
                "confidence": 0.0,
                "error": "Could not understand audio"
            }
        except sr.RequestError as e:
            logger.error(f"Google Speech Recognition request error: {str(e)}")
            raise ValueError(f"Speech recognition service error: {str(e)}")

    async def detect_language(self, audio_data: bytes, audio_format: str = "wav") -> str:
        """
        Attempt to detect the language of the audio

        Args:
            audio_data: Raw audio bytes
            audio_format: Audio format

        Returns:
            Detected language code (e.g., "en", "es")
        """
        # Try transcribing with multiple languages and pick the one with highest confidence
        best_lang = "en"
        best_confidence = 0.0

        test_languages = ["en", "es", "fr", "de", "zh"]  # Common languages to test

        for lang in test_languages:
            try:
                result = await self.transcribe_audio(
                    audio_data,
                    audio_format,
                    language=lang,
                    alternative_count=1
                )

                if result["confidence"] > best_confidence:
                    best_confidence = result["confidence"]
                    best_lang = lang

            except Exception as e:
                logger.debug(f"Language detection failed for {lang}: {str(e)}")
                continue

        logger.info(f"Detected language: {best_lang} (confidence: {best_confidence:.2f})")

        return best_lang

    def adjust_for_ambient_noise(self, audio_source, duration: float = 1.0):
        """
        Adjust recognizer for ambient noise
        Useful for real-time voice recording

        Args:
            audio_source: AudioSource object
            duration: Duration in seconds to analyze ambient noise
        """
        self.recognizer.adjust_for_ambient_noise(audio_source, duration=duration)
        logger.info(f"Adjusted for ambient noise (duration: {duration}s)")

    async def validate_audio(
        self,
        audio_data: bytes,
        min_duration: float = 0.5,
        max_duration: float = 30.0
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate audio data before transcription

        Args:
            audio_data: Raw audio bytes
            min_duration: Minimum acceptable duration in seconds
            max_duration: Maximum acceptable duration in seconds

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check if audio data is not empty
            if not audio_data or len(audio_data) == 0:
                return False, "Audio data is empty"

            # Try to load audio with pydub
            audio = AudioSegment.from_wav(io.BytesIO(audio_data))

            # Check duration
            duration = len(audio) / 1000.0  # Convert milliseconds to seconds

            if duration < min_duration:
                return False, f"Audio too short ({duration:.2f}s). Minimum: {min_duration}s"

            if duration > max_duration:
                return False, f"Audio too long ({duration:.2f}s). Maximum: {max_duration}s"

            # Check if audio has content (not silent)
            if audio.dBFS < -50:  # Very quiet audio
                return False, "Audio appears to be silent or too quiet"

            return True, None

        except Exception as e:
            logger.error(f"Audio validation error: {str(e)}")
            return False, f"Invalid audio format: {str(e)}"

    async def enhance_audio(self, audio_data: bytes, audio_format: str = "wav") -> bytes:
        """
        Enhance audio quality for better recognition

        Args:
            audio_data: Raw audio bytes
            audio_format: Audio format

        Returns:
            Enhanced audio bytes in WAV format
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format=audio_format)

            # Normalize volume
            normalized = audio.normalize()

            # Apply high-pass filter to reduce low-frequency noise
            filtered = normalized.high_pass_filter(80)

            # Convert to mono if stereo
            if filtered.channels > 1:
                filtered = filtered.set_channels(1)

            # Set sample rate to 16kHz (optimal for speech recognition)
            filtered = filtered.set_frame_rate(16000)

            # Export enhanced audio
            output = io.BytesIO()
            filtered.export(output, format="wav")
            output.seek(0)

            logger.info("Enhanced audio quality for transcription")

            return output.read()

        except Exception as e:
            logger.error(f"Audio enhancement error: {str(e)}")
            # Return original audio if enhancement fails
            return audio_data

    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages with their full names"""
        language_names = {
            "en": "English (US)",
            "en-gb": "English (UK)",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese (Brazil)",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese (Simplified)",
        }
        return language_names

    async def process_voice_query(
        self,
        audio_data: bytes,
        audio_format: str = "wav",
        language: str = "en",
        enhance: bool = True
    ) -> Dict[str, any]:
        """
        Complete voice query processing pipeline

        Args:
            audio_data: Raw audio bytes
            audio_format: Audio format
            language: Language code
            enhance: Whether to enhance audio before transcription

        Returns:
            Dictionary with complete processing results
        """
        # Validate audio
        is_valid, error = await self.validate_audio(audio_data)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "text": "",
                "confidence": 0.0
            }

        # Enhance audio if requested
        if enhance:
            audio_data = await self.enhance_audio(audio_data, audio_format)
            audio_format = "wav"

        # Transcribe
        result = await self.transcribe_audio(
            audio_data,
            audio_format,
            language,
            alternative_count=3
        )

        return {
            "success": True,
            "text": result["text"],
            "alternatives": result.get("alternatives", []),
            "confidence": result.get("confidence", 0.0),
            "language": result.get("language", language),
            "duration": result.get("duration", 0.0)
        }
