# Voice Dictation → Clean Text Tool (Windows + ChatGPT Enterprise / Azure)

This file serves as context for GitHub Copilot.

It has three purposes:

1. Document what's already available in open source that is similar to what I want.
2. Specify exactly what I want Copilot to help me build **now**.
3. Note that I have **Azure access**, which we may use (Azure OpenAI, Azure Speech) instead of or in addition to the standard OpenAI API.

I will add this file to my repo to give GitHub Copilot clear context.

---

## 0. Repo Setup (Before Coding)

I **don't have a repo yet** for this tool. I plan to:

1. Create a new GitHub repo, e.g. `voice-dictation-cleaner`.
2. Clone it locally and open it in VS Code.
3. Add this file (`voice_dictation_copilot_context.md`) at the repo root so Copilot can use it as context.
4. Initialize a Python virtual environment and `requirements.txt` as described below.

Copilot, please assume this repo structure when creating files.

---

## 1. Existing Open Source Options (Context Only)

These are examples of existing projects that are close to what I want. They are **not required dependencies**, just context to show the problem space.

### 1.1. Dictate (Closest Overall Match Conceptually)

- Repo: `3choff/dictate`
- Windows desktop dictation app built with Tauri & Rust.
- Provides:
  - Global hotkeys for dictation.
  - Dictation into any active application (seamless text insertion).
  - Multiple STT providers (Groq, Deepgram, Gemini, etc.).
  - Text rewrite support with modes like:
    - Grammar correction
    - Professional tone
    - Polite tone
    - Casual tone
    - Structured & organized
  - A text rewrite hotkey (e.g., `Ctrl+Shift+R`) to rewrite selected text via AI providers.

Why it matters for this spec:
- It demonstrates the exact kind of workflow I want:
  - Dictation → type at cursor, plus
  - LLM-based rewriting modes.
- However, it is not specifically wired to **ChatGPT Enterprise / Azure OpenAI Enterprise** out-of-the-box.

### 1.2. OmniDictate

- Repo: `gurjar1/OmniDictate`
- Free, open-source, Windows-focused GUI dictation tool.
- Uses `faster-whisper` locally (no cloud) for speech-to-text.
- Types text directly into the active window; global hotkey support.
- Strong privacy posture (local STT).

Limitation for my needs:
- Pure STT (speech → raw transcript) with punctuation but **no LLM cleanup**.
- I still want an automatic cleanup step using my Enterprise LLM.

### 1.3. OpenWhispr

- Repo: `HeroTools/open-whispr`
- Cross-platform desktop dictation app using Whisper (local or cloud).
- Supports global hotkeys and auto-paste at cursor.
- Privacy-aware, can be configured to use local models.

Limitation for my needs:
- Same as OmniDictate: strong STT, but no integrated LLM rewrite/cleanup.

### 1.4. Other Whisper Dictation Repos

Examples (not exhaustive):

- `haliul/windows-whisper-dictation`
- `xyc0123456789/whisper_dictate`
- `themanyone/whisper_dictation`

Common theme:
- All focus on **speech-to-text + type/paste into active window**.
- None are tailored to:
  - ChatGPT Enterprise / Azure OpenAI Enterprise as the LLM, and
  - Automatic cleanup into polished, email-ready / prompt-ready text.

---

## 2. What I Want Copilot to Help Me Build

> **Goal**: A small Windows tool that lets me press a hotkey, speak for a few seconds, and then automatically paste **cleaned-up text** at my cursor in any application (VS Code, browser, Teams, Outlook, Word, etc.).
>
> I specifically want to use my **Enterprise LLM** for the cleanup step:
> - Either **ChatGPT Enterprise (OpenAI API)**, **Azure OpenAI**, or make it easy to support either.

This is primarily a **personal productivity tool**, not a product I'm shipping. Simplicity is more important than UI polish.

### 2.1. High-Level Behavior

When I press a global hotkey (for example, `Ctrl+Shift+D`):

1. Start recording audio from my default microphone.
2. Stop recording after a short duration (configurable, e.g. 8–12 seconds) or on another keypress if we later add that.
3. Convert audio → raw text using **speech-to-text**:
   - Initial implementation can use:
     - OpenAI audio transcription endpoint (Enterprise tenant), **or**
     - Azure OpenAI Speech / Azure Cognitive Services Speech, **or**
     - (Future) local Whisper/faster-whisper.
   - For **v1**, it's fine to assume the standard OpenAI audio endpoint or Azure OpenAI; just make it easy to swap.
4. Send the raw transcription to a **text model in my Enterprise environment** (OpenAI or Azure) to:
   - Remove filler words (`um`, `uh`, `like`, `you know`, etc.).
   - Add punctuation and capitalization.
   - Break up run-on sentences.
   - Preserve meaning and technical terms.
   - Produce clear, concise, professional text suitable for emails, chats, and prompts.
5. Copy the cleaned text to the **clipboard**.
6. Automatically **paste** it at the current cursor location in whatever window is focused.

From the user perspective:

> Focus any text field → press hotkey → speak → short pause → cleaned text appears where the cursor was.

### 2.2. Modes (Enterprise vs Personal)

I want to support two **modes** of operation:

1. **Enterprise mode** (for IP-sensitive / work content)
   - Uses my **Enterprise** OpenAI / Azure OpenAI endpoint.
   - Intended for company IP, code, specs, emails, etc.
2. **Personal mode** (for non-IP content)
   - Could use:
     - A different API key / endpoint, or
     - A cheaper model or even local-only STT (in future).
   - Intended for personal emails, notes, etc.

For **v1**, it's enough to support:

- A `--mode enterprise` flag and
- A `--mode personal` flag

plus different model / key settings based on mode. We can wire multiple hotkeys later (e.g., one shortcut per mode).

### 2.3. Technical Constraints

- OS: **Windows 10/11**.
- Language: **Python** for the core logic.
- Use the official **OpenAI Python client** (and/or Azure SDKs) where appropriate.
- Secrets / configuration:
  - **Do not** hard-code API keys.
  - Read keys and endpoints from environment variables:
    - `OPENAI_API_KEY`
    - `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, etc. (optional, if using Azure).
  - Optionally support `.env` via `python-dotenv`.
- The tool must be **application-agnostic**:
  - It should work in VS Code, browsers, Teams, Outlook, Word, Notepad, etc.
  - The "paste at cursor" behavior should not depend on any specific app integration.
- For **global hotkey + paste**, I'm fine using **AutoHotkey** in `tools/dictation.ahk`.

---

## 3. Project Structure

I want a minimal but organized project structure, like this:

```text
voice-dictation-cleaner/
  ├─ src/
  │   ├─ main.py            # entry point (called by hotkey or CLI)
  │   ├─ audio_utils.py     # microphone recording utilities
  │   ├─ llm_utils.py       # OpenAI / Azure OpenAI calls (transcription + cleanup)
  │   ├─ config.py          # configuration (durations, model names, prompts, mode handling)
  ├─ tools/
  │   └─ dictation.ahk      # AutoHotkey script to bind global hotkey and paste
  ├─ requirements.txt
  ├─ README.md
  ├─ voice_dictation_copilot_context.md
  ├─ voice_dictation_roadmap.md   # (separate file with future roadmap)
```
