#!/usr/bin/env python3
"""handwriting-ocr-mcp 설치 스크립트 (macOS/Linux/Windows)"""

import os
import platform
import shutil
import subprocess
import sys


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    print(f"  > {' '.join(cmd)}")
    return subprocess.run(cmd, check=check)


def install_uv() -> str:
    """uv를 설치하고 경로를 반환한다."""
    uv = shutil.which("uv")
    if uv:
        return uv

    print("uv가 설치되어 있지 않습니다. 설치합니다...")
    if platform.system() == "Windows":
        run(["powershell", "-ExecutionPolicy", "ByPass", "-c",
             "irm https://astral.sh/uv/install.ps1 | iex"])
    else:
        run(["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"])

    # 설치 후 PATH에 추가
    local_bin = os.path.join(os.path.expanduser("~"), ".local", "bin")
    cargo_bin = os.path.join(os.path.expanduser("~"), ".cargo", "bin")
    for p in [local_bin, cargo_bin]:
        if os.path.isdir(p) and p not in os.environ.get("PATH", ""):
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")

    uv = shutil.which("uv")
    if not uv:
        print("ERROR: uv 설치에 실패했습니다. https://docs.astral.sh/uv/ 에서 수동 설치하세요.")
        sys.exit(1)

    print("uv 설치 완료")
    return uv


def sync_dependencies(uv: str) -> None:
    print("\n의존성을 설치합니다...")
    run([uv, "sync", "--extra", "dev", "--extra", "tesseract"])
    print("의존성 설치 완료")


def create_env_file() -> None:
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("\n.env 파일이 생성되었습니다.")
        print("Google Vision API를 사용하려면 .env 파일에 GOOGLE_API_KEY를 설정하세요.")


def check_tesseract() -> None:
    if shutil.which("tesseract"):
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        version = result.stdout.splitlines()[0] if result.stdout else "unknown"
        print(f"Tesseract: {version}")
        return

    print("\nTesseract OCR이 설치되어 있지 않습니다.")
    system = platform.system()

    if system == "Darwin":
        hint = "brew install tesseract tesseract-lang"
    elif system == "Linux":
        hint = "sudo apt install tesseract-ocr tesseract-ocr-kor"
    elif system == "Windows":
        hint = "https://github.com/UB-Mannheim/tesseract/wiki 에서 설치 후 PATH에 추가"
    else:
        hint = "OS에 맞는 방법으로 Tesseract를 설치하세요"

    if not sys.stdin.isatty():
        print(f"Tesseract 수동 설치가 필요합니다: {hint}")
        return

    answer = input(f"Tesseract를 설치할까요? ({hint}) (y/N) ").strip().lower()
    if answer == "y":
        if system == "Darwin":
            run(["brew", "install", "tesseract", "tesseract-lang"])
        elif system == "Linux":
            run(["sudo", "apt", "install", "-y", "tesseract-ocr", "tesseract-ocr-kor"])
        elif system == "Windows":
            print(f"Windows에서는 수동 설치가 필요합니다: {hint}")
            return
        print("Tesseract 설치 완료")
    else:
        print("Tesseract 설치를 건너뜁니다. Google Vision API 키가 필요합니다.")


def run_tests(uv: str) -> bool:
    print("\n테스트를 실행합니다...")
    result = run([uv, "run", "python", "-m", "pytest", "tests/", "-q"], check=False)
    return result.returncode == 0


def main() -> None:
    print("=== handwriting-ocr-mcp 설치 ===\n")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    uv = install_uv()
    run([uv, "--version"])

    sync_dependencies(uv)
    create_env_file()
    check_tesseract()

    ok = run_tests(uv)

    if ok:
        print("\n=== 설치 완료 ===")
        print("\n서버 실행: fastmcp run src/handwriting_ocr_mcp/server.py:mcp")
    else:
        print("\n=== 설치 완료 (테스트 실패 항목이 있습니다) ===")


if __name__ == "__main__":
    main()
