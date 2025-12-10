"""
LLM utilities for transcription and text cleanup.
Supports both OpenAI and Azure OpenAI.
"""
from openai import OpenAI, AzureOpenAI
from typing import Optional
from config import ModeConfig, Config


class LLMClient:
    """Client for LLM operations (transcription and cleanup)."""
    
    def __init__(self, config: ModeConfig):
        """
        Initialize the LLM client based on configuration.
        
        Args:
            config: Mode configuration (Enterprise or Personal)
        """
        self.config = config
        
        if config.use_azure:
            # Azure OpenAI client
            self.client = AzureOpenAI(
                api_key=config.azure_openai_api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=config.azure_openai_endpoint
            )
        else:
            # Standard OpenAI client
            self.client = OpenAI(api_key=config.openai_api_key)
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using Whisper.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        print(f"Transcribing audio using {self.config.mode_name} mode...")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                if self.config.use_azure:
                    # Azure OpenAI Whisper
                    transcription = self.client.audio.transcriptions.create(
                        model=self.config.azure_audio_deployment_name,
                        file=audio_file
                    )
                else:
                    # OpenAI Whisper
                    transcription = self.client.audio.transcriptions.create(
                        model=self.config.openai_audio_model,
                        file=audio_file
                    )
            
            transcribed_text = transcription.text
            print(f"Transcription: {transcribed_text}")
            return transcribed_text
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise
    
    def cleanup_text(self, raw_text: str) -> str:
        """
        Clean up transcribed text using LLM.
        
        Args:
            raw_text: Raw transcription text
            
        Returns:
            Cleaned and polished text
        """
        print(f"Cleaning up text using {self.config.mode_name} mode...")
        
        try:
            # Format the cleanup prompt
            prompt = Config.CLEANUP_PROMPT.format(transcription=raw_text)
            
            if self.config.use_azure:
                # Azure OpenAI
                response = self.client.chat.completions.create(
                    model=self.config.azure_deployment_name,
                    messages=[
                        {"role": "system", "content": "You are a text cleanup assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
            else:
                # OpenAI
                response = self.client.chat.completions.create(
                    model=self.config.openai_model,
                    messages=[
                        {"role": "system", "content": "You are a text cleanup assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
            
            cleaned_text = response.choices[0].message.content.strip()
            print(f"Cleaned text: {cleaned_text}")
            return cleaned_text
            
        except Exception as e:
            print(f"Error during text cleanup: {e}")
            raise
    
    def process_dictation(self, audio_file_path: str) -> str:
        """
        Complete dictation pipeline: transcribe and cleanup.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Final cleaned text
        """
        # Step 1: Transcribe audio
        raw_text = self.transcribe_audio(audio_file_path)
        
        # Step 2: Clean up text
        cleaned_text = self.cleanup_text(raw_text)
        
        return cleaned_text
