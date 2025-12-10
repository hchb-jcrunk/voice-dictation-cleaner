"""
Voice Dictation Cleaner - Main Entry Point

This script orchestrates the complete voice dictation workflow:
1. Record audio from microphone
2. Transcribe using Whisper (OpenAI or Azure)
3. Clean up text using LLM
4. Copy to clipboard (ready for paste)
"""
import sys
import argparse
import pyperclip
from audio_utils import AudioRecorder
from llm_utils import LLMClient
from config import Config


def main():
    """Main entry point for voice dictation."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Voice dictation with LLM cleanup")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["enterprise", "personal"],
        default="enterprise",
        help="Operation mode: enterprise or personal"
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Recording duration in seconds (overrides config)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output audio file path (for debugging)"
    )
    
    args = parser.parse_args()
    
    # Get configuration for the selected mode
    mode_config = Config.get_mode_config(args.mode)
    
    # Validate configuration
    if not Config.validate_mode_config(mode_config):
        print("\nPlease set the required environment variables in a .env file or system environment.")
        sys.exit(1)
    
    # Override duration if specified
    if args.duration:
        mode_config.recording_duration = args.duration
    
    print(f"\n=== Voice Dictation Cleaner ===")
    print(f"Mode: {args.mode.upper()}")
    print(f"Duration: {mode_config.recording_duration} seconds")
    print(f"Provider: {'Azure OpenAI' if mode_config.use_azure else 'OpenAI'}")
    print("=" * 32 + "\n")
    
    try:
        # Step 1: Record audio
        recorder = AudioRecorder(
            sample_rate=mode_config.sample_rate,
            channels=mode_config.channels
        )
        audio_file = recorder.record(
            duration=mode_config.recording_duration,
            output_path=args.output
        )
        
        # Step 2: Process dictation (transcribe + cleanup)
        llm_client = LLMClient(mode_config)
        cleaned_text = llm_client.process_dictation(audio_file)
        
        # Step 3: Copy to clipboard
        pyperclip.copy(cleaned_text)
        print("\n✓ Cleaned text copied to clipboard!")
        print(f"\nFinal text:\n{cleaned_text}")
        
        # Clean up temporary audio file (unless user specified output path)
        if not args.output:
            recorder.cleanup_temp_file(audio_file)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
