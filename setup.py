#!/usr/bin/env python3
"""handwriting-ocr-mcp installation script (macOS/Linux/Windows)"""

import json
import os
import platform
import shutil
import subprocess
import sys
from typing import Any, Dict, cast


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"  > {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, text=True)


def install_uv() -> str:
    """Installs uv and returns its path."""
    uv = shutil.which("uv")
    if uv:
        return uv

    print("uv is not installed. Installing...")
    try:
        # Try brew first on macOS
        if platform.system() == "Darwin" and shutil.which("brew"):
            try:
                print("Attempting to install uv via Homebrew...")
                run(["brew", "install", "uv"])
                uv = shutil.which("uv")
                if uv:
                    print("uv installation via Homebrew complete")
                    return uv
            except subprocess.CalledProcessError:
                print("Homebrew installation failed. Retrying with official script.")

        if platform.system() == "Windows":
            run(["powershell", "-ExecutionPolicy", "ByPass", "-c",
                 "irm https://astral.sh/uv/install.ps1 | iex"])
        else:
            # Add timeout settings: connect 10s, max time 300s
            run(["sh", "-c", "curl -LsSf --connect-timeout 10 --max-time 300 https://astral.sh/uv/install.sh | sh"])
    except (subprocess.CalledProcessError, KeyboardInterrupt):
        print("\n\n!!! Error occurred during official installation script execution (network instability, etc.).")
        print("Attempting alternative installation via pip...")
        try:
            run([sys.executable, "-m", "pip", "install", "uv"])
        except subprocess.CalledProcessError:
            print("pip installation also failed.")

    # Add to PATH after installation (for current process)
    local_bin = os.path.join(os.path.expanduser("~"), ".local", "bin")
    cargo_bin = os.path.join(os.path.expanduser("~"), ".cargo", "bin")
    
    path_modified = False
    for p in [local_bin, cargo_bin]:
        if os.path.isdir(p) and p not in os.environ.get("PATH", ""):
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
            path_modified = True

    uv = shutil.which("uv")
    if not uv:
        # Since it might have been installed via pip, complex checks like sys.executable based bin are skipped
        # If not in PATH, guide for manual installation
        print("ERROR: Failed to install uv. Please try the following methods:")
        print("  1. Check network connection")
        print("  2. pip install uv (manual execution)")
        print("  3. Download binary directly from https://docs.astral.sh/uv/")
        sys.exit(1)

    assert uv is not None
    print("uv installation complete")
    if path_modified:
        print(f"NOTE: 'uv' installed at {os.path.dirname(uv)}. Please restart terminal or add to PATH.")

    assert uv is not None
    return uv


def check_venv() -> None:
    """Checks if venv Python path matches current directory, recreates if mismatch."""
    venv_dir = os.path.join(os.getcwd(), ".venv")
    if not os.path.isdir(venv_dir):
        return

    if platform.system() == "Windows":
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_path = os.path.join(venv_dir, "bin", "python3")

    if not os.path.exists(python_path):
        return

    real_python = os.path.realpath(python_path)
    if os.path.exists(real_python):
        return

    print("Existing .venv Python path is invalid. Recreating venv...")
    shutil.rmtree(venv_dir)
    print(".venv deletion complete")


def sync_dependencies(uv: str) -> None:
    check_venv()
    print("\nInstalling dependencies...")
    run([uv, "sync", "--extra", "dev", "--extra", "tesseract"])
    print("Dependencies installation complete")


def create_env_file() -> None:
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("\n.env file created.")
        print("To use Google Vision API, set GOOGLE_API_KEY in .env file.")


def configure_credentials() -> None:
    """Interactively configures Google Cloud credentials."""
    print("\n--- Google Cloud Vision API Setup ---")
    
    # Check if already configured
    current_key = _read_env_value("GOOGLE_APPLICATION_CREDENTIALS")
    if current_key and os.path.exists(current_key):
        print(f"Credentials already configured: {current_key}")
        if sys.stdin.isatty():
            answer = input("Do you want to reconfigure? (y/N) ").strip().lower()
            if answer != "y":
                return
        else:
            return

    if not sys.stdin.isatty():
        print("Skipping interactive credential setup (not a TTY).")
        return

    print("To use Google Vision API, you need a Service Account Key (JSON file).")
    print("If you don't have one, please refer to docs/google_vision_setup.md.")
    
    answer = input("Do you have a Service Account JSON key file ready? (y/N) ").strip().lower()
    if answer != "y":
        print("Skipping credential setup. You can set GOOGLE_APPLICATION_CREDENTIALS in .env later.")
        return

    while True:
        path_input = input("Enter the path to your JSON key file: ").strip().strip("'").strip('"')
        if not path_input:
            print("Skipping credential setup.")
            return

        json_path = os.path.abspath(os.path.expanduser(path_input))
        if os.path.isfile(json_path):
            break
        print(f"Error: File not found at {json_path}")
        retry = input("Try again? (Y/n) ").strip().lower()
        if retry == "n":
            return

    # Create keys directory
    keys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")
    os.makedirs(keys_dir, exist_ok=True)
    
    # Ask to copy
    filename = os.path.basename(json_path)
    dest_path = os.path.join(keys_dir, filename)
    
    use_path = json_path
    
    # Avoid overwriting if source and dest are same
    if os.path.abspath(json_path) != os.path.abspath(dest_path):
        print(f"\nRecommended: Copy this key to the project's secure 'keys/' directory.")
        print(f"Destination: {dest_path}")
        copy_ans = input("Copy file to project keys directory? (Y/n) ").strip().lower()
        if copy_ans != "n":
            try:
                shutil.copy2(json_path, dest_path)
                print(f"Key copied to {dest_path}")
                use_path = dest_path
            except Exception as e:
                print(f"Failed to copy file: {e}")
                print(f"Using original path: {json_path}")

    # Update .env
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    # Read existing content
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    # Update or append GOOGLE_APPLICATION_CREDENTIALS
    key_found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("GOOGLE_APPLICATION_CREDENTIALS="):
             new_lines.append(f'GOOGLE_APPLICATION_CREDENTIALS="{use_path}"\n')
             key_found = True
        else:
            new_lines.append(line)
    
    if not key_found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f'GOOGLE_APPLICATION_CREDENTIALS="{use_path}"\n')

    with open(env_path, "w") as f:
        f.writelines(new_lines)
    
    print(f"\nUpdated .env with GOOGLE_APPLICATION_CREDENTIALS=\"{use_path}\"")



def configure_language() -> None:
    """Configures default OCR language."""
    print("\n--- Default Language Setup ---")
    
    current_lang = _read_env_value("OCR_DEFAULT_LANGUAGE")
    if current_lang:
        print(f"Current default language: {current_lang}")
        if sys.stdin.isatty():
            answer = input("Do you want to change it? (y/N) ").strip().lower()
            if answer != "y":
                return
        else:
            return

    if not sys.stdin.isatty():
        print("Skipping language setup (not a TTY). Defaulting to 'en' if not set.")
        if not current_lang:
            _update_env_key("OCR_DEFAULT_LANGUAGE", "en")
        return

    default_lang = "en"
    print(f"Select default language code (e.g. en, ko, ja) [default: {default_lang}]")
    lang = input(f"Language code: ").strip()
    
    if not lang:
        lang = default_lang
    
    _update_env_key("OCR_DEFAULT_LANGUAGE", lang)
    print(f"Default language set to: {lang}")


def _update_env_key(key: str, value: str) -> None:
    """Updates or adds a key-value pair in .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
            
    key_found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
             new_lines.append(f'{key}="{value}"\n')
             key_found = True
        else:
            new_lines.append(line)
    
    if not key_found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f'{key}="{value}"\n')

    with open(env_path, "w") as f:
        f.writelines(new_lines)


def check_tesseract() -> None:
    if shutil.which("tesseract"):
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        version = result.stdout.splitlines()[0] if result.stdout else "unknown"
        print(f"Tesseract: {version}")
        return

    print("\nTesseract OCR is not installed.")
    system = platform.system()

    if system == "Darwin":
        hint = "brew install tesseract tesseract-lang"
    elif system == "Linux":
        hint = "sudo apt install tesseract-ocr tesseract-ocr-kor"
    elif system == "Windows":
        hint = "Install from https://github.com/UB-Mannheim/tesseract/wiki and add to PATH"
    else:
        hint = "Install Tesseract using method appropriate for your OS"

    if not sys.stdin.isatty():
        print(f"Manual Tesseract installation required: {hint}")
        return

    answer = input(f"Install Tesseract? ({hint}) (y/N) ").strip().lower()
    if answer == "y":
        if system == "Darwin":
            if not shutil.which("brew"):
                print("Error: Homebrew not installed. Install from https://brew.sh/.")
                return
            run(["brew", "install", "tesseract", "tesseract-lang"])
        elif system == "Linux":
            if not shutil.which("apt"):
                 print(f"Error: apt package manager not found. Manual installation required: {hint}")
                 return
            run(["sudo", "apt", "update"])
            run(["sudo", "apt", "install", "-y", "tesseract-ocr", "tesseract-ocr-kor"])
        elif system == "Windows":
            print(f"Manual installation required on Windows: {hint}")
            return
        
        # Verify installation
        if shutil.which("tesseract"):
             print("Tesseract installation complete")
        else:
             print("Warning: Attempted Tesseract installation but could not find in PATH.")
    else:
        print("Skipping Tesseract installation. Google Vision API key is required.")


def _get_claude_config_path() -> str:
    """Returns Claude Desktop config file path by OS."""
    system = platform.system()
    if system == "Darwin":
        return os.path.join(
            os.path.expanduser("~"),
            "Library", "Application Support", "Claude",
            "claude_desktop_config.json",
        )
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        if not appdata:
            appdata = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
        return os.path.join(appdata, "Claude", "claude_desktop_config.json")
    else:
        config_home = os.environ.get(
            "XDG_CONFIG_HOME",
            os.path.join(os.path.expanduser("~"), ".config"),
        )
        return os.path.join(config_home, "Claude", "claude_desktop_config.json")


def _read_env_value(key: str) -> str:
    """Reads and returns value for specific key from .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        return ""
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
    return ""


def configure_claude_desktop(uv: str) -> None:
    """Registers MCP server to Claude Desktop config file."""
    config_path = _get_claude_config_path()
    project_root = os.path.dirname(os.path.abspath(__file__))

    config_dir = os.path.dirname(config_path)
    if not os.path.isdir(config_dir):
        print(f"\nClaude Desktop config directory does not exist: {config_dir}")
        print("Check if Claude Desktop is installed.")
        return

    # Read existing config
    config: Dict[str, Any] = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            try:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    config = cast(Dict[str, Any], loaded)
                else:
                    config = {}
            except json.JSONDecodeError:
                print(f"Warning: {config_path} file is not valid JSON.")
                if sys.stdin.isatty():
                    answer = input("Overwrite existing file? (y/N) ").strip().lower()
                    if answer != "y":
                        print("Skipping Claude Desktop configuration.")
                        return
                else:
                    print("Skipping Claude Desktop configuration.")
                    return
                config = {}

    # Configure server entry
    server_path = os.path.join(project_root, "src", "handwriting_ocr_mcp", "server.py")
    server_entry: dict = {
        "command": uv,
        "args": [
            "run",
            "--project",
            project_root,
            "fastmcp",
            "run",
            f"{server_path}:mcp",
        ],
    }

    # Check if change is needed
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    if config["mcpServers"].get("handwriting-ocr-mcp") == server_entry:
        print(f"\nClaude Desktop config is already up to date: {config_path}")
        return

    # User confirmation
    print(f"\nUpdating Claude Desktop config file: {config_path}")
    print(f"  command: {uv}")
    print(f"  project: {project_root}")
    
    if sys.stdin.isatty():
        if "handwriting-ocr-mcp" in config.get("mcpServers", {}):
            answer = input("Update existing handwriting-ocr-mcp config? (Y/n) ").strip().lower()
        else:
            answer = input("Add handwriting-ocr-mcp config? (Y/n) ").strip().lower()
        if answer == "n":
            print("Skipping Claude Desktop configuration.")
            return

    # Save config
    config["mcpServers"]["handwriting-ocr-mcp"] = server_entry

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("Claude Desktop configuration complete")
    print("NOTE: Restart Claude Desktop to apply settings.")


def run_tests(uv: str) -> bool:
    print("\nRunning tests...")
    # uv run executes within venv, so use python -m pytest
    result = run([uv, "run", "python", "-m", "pytest", "tests/", "-q"], check=False)
    return result.returncode == 0


def main() -> None:
    print("=== handwriting-ocr-mcp installation ===\n")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    uv = install_uv()
    run([uv, "--version"])

    sync_dependencies(uv)
    create_env_file()
    configure_credentials()
    configure_language()
    check_tesseract()
    configure_claude_desktop(uv)

    ok = run_tests(uv)

    if ok:
        print("\n=== Installation Complete ===")
        print("\nRun server: uv run fastmcp run src/handwriting_ocr_mcp/server.py:mcp")
    else:
        print("\n=== Installation Complete (with test failures) ===")


if __name__ == "__main__":
    main()
