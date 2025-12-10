"""
Audio recording utilities for voice dictation.
"""
import pyaudio
import wave
import tempfile
import os
from typing import Optional


class AudioRecorder:
    """Records audio from the default microphone."""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        """
        Initialize the audio recorder.
        
        Args:
            sample_rate: Sample rate in Hz (16000 is good for speech)
            channels: Number of audio channels (1 for mono, 2 for stereo)
            chunk_size: Size of audio chunks to read
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16  # 16-bit audio
        
    def record(self, duration: int, output_path: Optional[str] = None) -> str:
        """
        Record audio for the specified duration.
        
        Args:
            duration: Recording duration in seconds
            output_path: Path to save the recording (optional, uses temp file if not provided)
            
        Returns:
            Path to the recorded audio file
        """
        # Use temporary file if no path specified
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
        
        print(f"Recording for {duration} seconds...")
        
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        try:
            # Open audio stream
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            num_chunks = int(self.sample_rate / self.chunk_size * duration)
            
            # Record audio
            for _ in range(num_chunks):
                data = stream.read(self.chunk_size)
                frames.append(data)
            
            # Stop and close stream
            stream.stop_stream()
            stream.close()
            
            # Save to WAV file
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
            
            print(f"Recording saved to: {output_path}")
            
        finally:
            # Clean up
            audio.terminate()
        
        return output_path
    
    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Remove a temporary audio file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            print(f"Warning: Could not remove temporary file {file_path}: {e}")
