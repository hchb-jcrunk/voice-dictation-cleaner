; Voice Dictation Cleaner - AutoHotkey Script
; 
; This script provides global hotkeys for voice dictation:
; - Ctrl+Shift+D: Dictation in Enterprise mode
; - Ctrl+Alt+D: Dictation in Personal mode
;
; Prerequisites:
; 1. Python 3.8+ installed and in PATH
; 2. Python virtual environment activated with required packages
; 3. .env file configured with API keys
;
; Configuration:
; - Update PYTHON_EXE to point to your Python executable
; - Update SCRIPT_PATH to point to your main.py location

; Configuration variables
PYTHON_EXE := "python"  ; Or full path like "C:\Python311\python.exe" or ".\venv\Scripts\python.exe"
SCRIPT_PATH := "..\src\main.py"  ; Adjust if running from different location

; Ctrl+Shift+D: Enterprise Mode Dictation
^+d::
{
    RunDictation("enterprise")
    return
}

; Ctrl+Alt+D: Personal Mode Dictation
^!d::
{
    RunDictation("personal")
    return
}

; Function to run dictation and auto-paste
RunDictation(mode)
{
    global PYTHON_EXE, SCRIPT_PATH
    
    ; Show a tooltip to indicate recording has started
    ToolTip, Recording... (mode: %mode%)
    
    ; Run the Python script (this will block until complete)
    ; The script will copy cleaned text to clipboard
    RunWait, %PYTHON_EXE% %SCRIPT_PATH% --mode %mode%, , Hide
    
    ; Remove tooltip
    ToolTip
    
    ; Small delay to ensure clipboard is ready
    Sleep, 100
    
    ; Paste the cleaned text at the current cursor position
    Send, ^v
    
    return
}

; Ctrl+Shift+X: Exit this script
^+x::
{
    ToolTip, Exiting Voice Dictation Cleaner...
    Sleep, 1000
    ExitApp
}

; Show startup message
ToolTip, Voice Dictation Cleaner loaded.`nCtrl+Shift+D = Enterprise`nCtrl+Alt+D = Personal`nCtrl+Shift+X = Exit
SetTimer, RemoveToolTip, 3000
return

RemoveToolTip:
SetTimer, RemoveToolTip, Off
ToolTip
return
