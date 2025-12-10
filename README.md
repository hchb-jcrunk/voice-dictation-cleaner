# Voice Dictation Cleaner

A Windows voice dictation tool that uses Enterprise LLM (OpenAI or Azure OpenAI) to clean up speech-to-text transcriptions for professional communication.

## Features

- 🎤 **Quick Voice Input**: Press a hotkey, speak, and get cleaned text pasted at your cursor
- 🏢 **Enterprise & Personal Modes**: Separate configurations for work and personal use
- 🤖 **LLM-Powered Cleanup**: Removes filler words, adds punctuation, and polishes text
- 🔒 **Privacy-Aware**: Choose between Enterprise (IP-safe) and Personal modes
- 🌐 **Flexible Backend**: Supports both OpenAI and Azure OpenAI
- 📝 **Application-Agnostic**: Works in any Windows application (VS Code, browsers, Teams, Outlook, etc.)

## How It Works

1. Press hotkey (`Ctrl+Shift+D` for Enterprise, `Ctrl+Alt+D` for Personal)
2. Speak for configured duration (default 10 seconds)
3. Audio is transcribed using Whisper
4. LLM cleans up the transcription (removes filler words, adds punctuation)
5. Cleaned text is automatically pasted at your cursor

## Prerequisites

- **Windows 10/11**
- **Python 3.8+**
- **AutoHotkey** (for global hotkeys)
- **OpenAI API access** or **Azure OpenAI access**
- **Microphone**

## Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/hchb-jcrunk/voice-dictation-cleaner.git
cd voice-dictation-cleaner
```

### 2. Set Up Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Install PyAudio (Windows)

PyAudio requires additional setup on Windows:

```powershell
# Install using pre-built wheel
pip install pipwin
pipwin install pyaudio
```

Or download a wheel from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Enterprise Mode (for work/IP-sensitive content)
OPENAI_API_KEY_ENTERPRISE=your-enterprise-api-key
OPENAI_MODEL_ENTERPRISE=gpt-4
OPENAI_AUDIO_MODEL_ENTERPRISE=whisper-1
RECORDING_DURATION_ENTERPRISE=10

# Optional: Use Azure OpenAI for Enterprise
USE_AZURE_ENTERPRISE=false
AZURE_OPENAI_API_KEY_ENTERPRISE=your-azure-key
AZURE_OPENAI_ENDPOINT_ENTERPRISE=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME_ENTERPRISE=gpt-4
AZURE_AUDIO_DEPLOYMENT_NAME_ENTERPRISE=whisper

# Personal Mode (for non-IP content)
OPENAI_API_KEY_PERSONAL=your-personal-api-key
OPENAI_MODEL_PERSONAL=gpt-4
OPENAI_AUDIO_MODEL_PERSONAL=whisper-1
RECORDING_DURATION_PERSONAL=10

# Optional: Use Azure OpenAI for Personal
USE_AZURE_PERSONAL=false
```

### 5. Install AutoHotkey

Download and install AutoHotkey from [https://www.autohotkey.com/](https://www.autohotkey.com/)

### 6. Configure AutoHotkey Script

Edit `tools/dictation.ahk` to set the correct paths:

```ahk
PYTHON_EXE := "C:\path\to\voice-dictation-cleaner\venv\Scripts\python.exe"
SCRIPT_PATH := "C:\path\to\voice-dictation-cleaner\src\main.py"
```

## Usage

### Running with AutoHotkey (Recommended)

1. Double-click `tools/dictation.ahk` to start the hotkey listener
2. Use hotkeys:
   - `Ctrl+Shift+D`: Dictate in **Enterprise** mode
   - `Ctrl+Alt+D`: Dictate in **Personal** mode
   - `Ctrl+Shift+X`: Exit the script

### Running from Command Line (Testing)

```powershell
# Enterprise mode
python src\main.py --mode enterprise

# Personal mode
python src\main.py --mode personal

# Custom duration
python src\main.py --mode enterprise --duration 15

# Save audio file for debugging
python src\main.py --mode personal --output recording.wav
```

## Configuration

### Recording Duration

Adjust recording length in `.env`:

```bash
RECORDING_DURATION_ENTERPRISE=12  # seconds
RECORDING_DURATION_PERSONAL=8
```

### Cleanup Prompt

Customize the cleanup behavior by editing `Config.CLEANUP_PROMPT` in `src/config.py`.

### Hotkeys

Modify hotkeys in `tools/dictation.ahk`:

```ahk
^+d::  ; Ctrl+Shift+D
^!d::  ; Ctrl+Alt+D
```

## Troubleshooting

### PyAudio Installation Issues

If PyAudio fails to install:
- Use `pipwin install pyaudio`
- Or download a pre-built wheel for your Python version

### No Audio Recording

- Check microphone permissions in Windows Settings
- Ensure your microphone is set as the default recording device
- Test with `python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"`

### API Key Errors

- Verify `.env` file is in the project root
- Check that environment variables are loaded: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY_ENTERPRISE'))"`

### AutoHotkey Not Working

- Ensure Python path in `dictation.ahk` is correct
- Run `python src\main.py --mode enterprise` from command line to test
- Check that AutoHotkey is running (look for icon in system tray)

## Architecture

```
voice-dictation-cleaner/
├── src/
│   ├── main.py           # Entry point and workflow orchestration
│   ├── audio_utils.py    # Audio recording with PyAudio
│   ├── llm_utils.py      # OpenAI/Azure transcription & cleanup
│   └── config.py         # Configuration and mode management
├── tools/
│   └── dictation.ahk     # AutoHotkey global hotkey script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── .gitignore
└── README.md
```

## Security Notes

- **Never commit `.env` file** to version control
- Use **Enterprise mode** for any work-related or IP-sensitive content
- Keep API keys secure and rotate them regularly
- Consider using Azure OpenAI for enhanced data privacy

## Future Enhancements

See `voice_dictation_roadmap.md` (if included) for planned features:
- Press-to-stop recording (instead of fixed duration)
- Local Whisper model support (offline mode)
- Custom cleanup modes (casual, formal, code, etc.)
- Multi-language support
- Wake word activation

## License

This is a personal productivity tool. Use at your own discretion.

## Acknowledgments

Inspired by open-source dictation projects:
- [3choff/dictate](https://github.com/3choff/dictate)
- [gurjar1/OmniDictate](https://github.com/gurjar1/OmniDictate)
- [HeroTools/open-whispr](https://github.com/HeroTools/open-whispr)
