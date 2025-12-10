"""
Configuration settings for voice dictation cleaner.
Handles Enterprise and Personal modes with environment variables.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class ModeConfig:
    """Configuration for a specific mode (Enterprise or Personal)."""
    mode_name: str
    
    # OpenAI settings
    openai_api_key: Optional[str]
    openai_model: str
    openai_audio_model: str
    
    # Azure OpenAI settings (optional)
    azure_openai_api_key: Optional[str]
    azure_openai_endpoint: Optional[str]
    azure_deployment_name: Optional[str]
    azure_audio_deployment_name: Optional[str]
    
    # Recording settings
    recording_duration: int = 10
    sample_rate: int = 16000
    channels: int = 1
    
    # Whether to use Azure instead of OpenAI
    use_azure: bool = False


class Config:
    """Main configuration manager."""
    
    # Enterprise mode configuration
    ENTERPRISE = ModeConfig(
        mode_name="enterprise",
        openai_api_key=os.getenv("OPENAI_API_KEY_ENTERPRISE"),
        openai_model=os.getenv("OPENAI_MODEL_ENTERPRISE", "gpt-4"),
        openai_audio_model=os.getenv("OPENAI_AUDIO_MODEL_ENTERPRISE", "whisper-1"),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY_ENTERPRISE"),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_ENTERPRISE"),
        azure_deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME_ENTERPRISE"),
        azure_audio_deployment_name=os.getenv("AZURE_AUDIO_DEPLOYMENT_NAME_ENTERPRISE"),
        recording_duration=int(os.getenv("RECORDING_DURATION_ENTERPRISE", "10")),
        use_azure=os.getenv("USE_AZURE_ENTERPRISE", "false").lower() == "true"
    )
    
    # Personal mode configuration
    PERSONAL = ModeConfig(
        mode_name="personal",
        openai_api_key=os.getenv("OPENAI_API_KEY_PERSONAL") or os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL_PERSONAL", "gpt-4"),
        openai_audio_model=os.getenv("OPENAI_AUDIO_MODEL_PERSONAL", "whisper-1"),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY_PERSONAL"),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_PERSONAL"),
        azure_deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME_PERSONAL"),
        azure_audio_deployment_name=os.getenv("AZURE_AUDIO_DEPLOYMENT_NAME_PERSONAL"),
        recording_duration=int(os.getenv("RECORDING_DURATION_PERSONAL", "10")),
        use_azure=os.getenv("USE_AZURE_PERSONAL", "false").lower() == "true"
    )
    
    # Cleanup prompt template
    CLEANUP_PROMPT = """Clean up the following voice transcription for professional use.

Requirements:
- Remove filler words (um, uh, like, you know, etc.)
- Add proper punctuation and capitalization
- Break up run-on sentences for clarity
- Fix obvious transcription errors
- Preserve all technical terms and specific names
- Keep the original meaning intact
- Make it suitable for emails, chats, and professional communication

Return ONLY the cleaned text, no explanations or meta-commentary.

Transcription:
{transcription}"""

    @staticmethod
    def get_mode_config(mode: str) -> ModeConfig:
        """Get configuration for the specified mode."""
        if mode.lower() == "enterprise":
            return Config.ENTERPRISE
        elif mode.lower() == "personal":
            return Config.PERSONAL
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'enterprise' or 'personal'.")
    
    @staticmethod
    def validate_mode_config(config: ModeConfig) -> bool:
        """Validate that a mode configuration has required credentials."""
        if config.use_azure:
            if not config.azure_openai_api_key or not config.azure_openai_endpoint:
                print(f"ERROR: Azure mode enabled for {config.mode_name} but missing credentials.")
                print("Required: AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
                return False
        else:
            if not config.openai_api_key:
                print(f"ERROR: OpenAI mode enabled for {config.mode_name} but missing API key.")
                print(f"Required: OPENAI_API_KEY_{config.mode_name.upper()}")
                return False
        return True
