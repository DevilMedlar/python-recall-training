#!/usr/bin/env python3
"""Launch script for Senpai Studio."""
import subprocess
import sys
import os
from pathlib import Path
import signal

def main():
    repo_root = Path(__file__).resolve().parent
    venv_python = repo_root / "venv" / "Scripts" / "python.exe"
    backend_script = repo_root / "studio" / "backend" / "main.py"
    
    # Use venv python if it exists
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    print("Starting Senpai Studio...")
    print("Open your browser at http://localhost:8000")
    
    try:
        p = subprocess.Popen([python_exe, str(backend_script)])
        p.wait()
    except KeyboardInterrupt:
        print("\nStopping Senpai Studio. Goodbye, Daddy.")
        p.kill()
    except Exception as e:
        print(f"Error starting studio: {e}")

if __name__ == "__main__":
    main()
