# Voice Dictation Cleaner – Roadmap

This file describes future enhancements and ideas for the voice dictation → clean text tool. It is **context for Copilot and future work**, not required for the initial v1 implementation.

---

## Phase POC – Lightweight Proof of Concept

**Goal:** Get a simple, end-to-end proof of concept working quickly, without worrying about Azure integration or fancy configuration.

Scope:

- Python script (`main.py`) that:
  - Records audio from the default microphone (fixed duration, e.g., 8–10 seconds).
  - Sends audio to the **OpenAI audio transcription API** using an Enterprise-safe API key.
  - Sends the raw transcript to an **OpenAI text model** (Enterprise) with a dictation-cleanup prompt.
  - Copies the cleaned text to the clipboard with `pyperclip`.
  - Prints the cleaned text to stdout.
- A minimal AutoHotkey script (`tools/dictation.ahk`) that:
  - Binds a single hotkey (e.g., `Ctrl+Shift+D`).
  - Runs `python main.py`.
  - Sends `Ctrl+V` to paste the clipboard content.

Notes:

- Only **one mode** initially (effectively "enterprise").
- Only **OpenAI** used (no Azure yet).
- No CLI flags or config files required beyond environment variable for `OPENAI_API_KEY`.
- This POC should be easy to build and iterate on first.

Once this Phase POC feels solid and useful, we can expand to the full v1 and beyond.

---

## Phase 0 – v1 (Core Functionality)

**Goal:** Have a working tool that is still simple, but more structured and configurable than the POC.

Scope (v1):

- Project structure:
  - `src/main.py` – entry point.
  - `src/audio_utils.py` – recording logic.
  - `src/llm_utils.py` – transcription and cleanup logic.
  - `src/config.py` – duration, model names, prompts.
  - `tools/dictation.ahk` – hotkey(s) and paste behavior.
- Two modes via CLI flag:
  - `--mode enterprise`
  - `--mode personal`
- Still primarily using **OpenAI (Enterprise)** for:
  - Audio transcription.
  - Text cleanup.
- Minimal logging / debug printing.
- Global hotkeys via AutoHotkey:
  - `Ctrl+Shift+D` → Enterprise mode.
  - `Ctrl+Alt+D` → Personal mode.

The detailed spec for this is in `voice_dictation_copilot_context.md`.  
Phase POC should naturally evolve into this structure.

---

## Phase 1 – Developer Experience Polish

### 1.1. Better Feedback & UX

- Show a small console or log message when:
  - Recording starts (e.g., "Listening…").
  - Recording ends.
  - Transcription starts/ends.
- Optionally integrate a lightweight notification:
  - System toast or tray balloon when:
    - Dictation is finished.
    - An error happens.

### 1.2. Configuration Improvements

- Move configuration into:
  - A `config.toml` or `config.yaml` file, OR
  - A `.env` file with overrides (in addition to environment variables).
- Allow changing:
  - Recording duration.
  - Default mode.
  - Model names / Azure deployment names.
  - Hotkey labels (documented, even if still implemented in AHK).

### 1.3. Simple Logging

- Add a `--debug` flag:
  - Logs raw transcript and cleaned text to the console.
  - Logs any API errors.

---

## Phase 2 – Azure Integration & Optional Local STT

This is where Azure really comes into play.

### 2.1. Azure OpenAI Integration

- Add dedicated functions in `llm_utils.py` for:
  - `transcribe_audio_with_azure_openai(...)` (if using Azure OpenAI for STT).
  - `clean_text_with_azure_openai(...)` for text cleanup.
- Support reading Azure settings:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_DEPLOYMENT_NAME`
  - `AZURE_OPENAI_API_VERSION`
- Add config flags (e.g. in `config.py`):
  - `STT_BACKEND = "openai" | "azure" | "local"`
  - `LLM_BACKEND = "openai" | "azure"`
- Behavior:
  - When `LLM_BACKEND = "azure"`, all cleanup runs through Azure OpenAI.
  - When `STT_BACKEND = "azure"`, audio transcription uses Azure's endpoint.

### 2.2. Azure Speech Service (Cognitive Services Speech) – STT

- Integrate **Azure Cognitive Services Speech** as a speech-to-text backend:
  - Potentially lower latency and highly robust STT.
  - Fully governed under Azure security/compliance.
- Add a new STT backend:
  - `STT_BACKEND = "openai"` (default from v1)
  - `STT_BACKEND = "azure_speech"`
  - `STT_BACKEND = "local_whisper"` (see 2.3)

### 2.3. Local Whisper / faster-whisper Mode

- Add an optional **local STT** backend using:
  - `whisper` or `faster-whisper`.
- Goals:
  - Keep all audio on-device.
  - Potential use cases:
    - Strict privacy mode for highly sensitive dictation.
    - Offline mode when network is flaky.

---

## Phase 3 – Smarter Modes & Content Awareness

### 3.1. Mode Profiles (Email / Chat / Prompt / Note)

- Add support for multiple **cleanup styles**, e.g.:
  - `email` – professional and slightly more verbose if needed.
  - `chat` – concise and conversational.
  - `prompt` – optimized for clarity as an LLM prompt.
  - `note` – keeps more structure, lists, and partial sentences.
- Implementation:
  - Profiles as variants of the system prompt.
  - Selectable via:
    - CLI flag (`--style email|chat|prompt|note`).
    - Different AHK scripts/keys (each calling main.py with a different `--style`).

### 3.2. IP Sensitivity Heuristics (Long-Term Experiment)

- Explore whether a lightweight classifier can label text as:
  - "Sensitive/IP" vs "Non-sensitive".
- Possible behavior:
  - If sensitive:
    - Force `mode = enterprise` and `LLM_BACKEND = "azure"` or "OpenAI Enterprise".
  - If not:
    - Allow `mode = personal` and/or cheaper models.

This is a stretch goal and should only be implemented if it can be done clearly and transparently.

---

## Phase 4 – UI & Packaging

### 4.1. Simple System Tray App (Optional)

- Wrap the Python script using a lightweight GUI framework or `pystray`:
  - System tray icon.
  - Right-click menu to:
    - Change mode (enterprise/personal).
    - Change STT/LLM backend (OpenAI/Azure/local).
    - Quit the app.
    - Open logs/config.

### 4.2. Packaging for Easier Install

- Use a packaging tool (e.g., `pyinstaller`) to:
  - Create a self-contained Windows executable.
  - Optionally reference or launch the AHK script.
- Provide a simple "installation & usage" README for future re-use or sharing with teammates.

---

## Phase 5 – Editor/Tool Integrations (Nice-to-Have)

### 5.1. VS Code Integration

- Add a VS Code task or extension that:
  - Calls the Python script.
  - Inserts cleaned text at the cursor in the active editor.
- Potential features:
  - Command Palette commands like "Dictate and Insert Text (Enterprise)" or "Dictate and Insert Text (Personal)".

### 5.2. CLI & File-Based Enhancements

- Add support for:
  - `--file <path.wav>`: transcribe + clean an existing audio file.
  - Stdin piping: accept text via stdin and perform **cleanup only** (no audio step).
- This would turn the tool into a general "text cleanup" CLI as well.

---

## Phase 6 – Advanced Ideas (Blue Sky)

- LLM-assisted **voice macros**:
  - "Create a Jira ticket that says …"
  - "Draft a Teams message to my team summarizing today's standup…"
- Multi-language support:
  - Detect language of speech.
  - Optionally translate to English while cleaning.
- Per-project profiles:
  - Different default styles/configs for different projects or directories (e.g., coding repo vs product-docs repo).

---

## Priority Order

1. **Phase POC** – Lightest possible OpenAI-only POC (get value immediately).
2. **Phase 0 (v1)** – Clean structure, two modes, still OpenAI-based.
3. **Phase 1** – UX improvements, configurable settings, basic logging.
4. **Phase 2** – Azure integration (Azure OpenAI + Azure Speech + local Whisper backend).
5. Later phases as time/need allows.
