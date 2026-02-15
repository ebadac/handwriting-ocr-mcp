#!/usr/bin/env python3
"""handwriting-ocr-mcp 설치 스크립트 (macOS/Linux/Windows)"""

import os
import platform
import shutil
import subprocess
import sys


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"  > {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, text=True)


def install_uv() -> str:
    """uv를 설치하고 경로를 반환한다."""
    uv = shutil.which("uv")
    if uv:
        return uv

    print("uv가 설치되어 있지 않습니다. 설치합니다...")
    try:
        # macOS의 경우 brew 우선 시도
        if platform.system() == "Darwin" and shutil.which("brew"):
            try:
                print("Homebrew로 uv 설치를 시도합니다...")
                run(["brew", "install", "uv"])
                uv = shutil.which("uv")
                if uv:
                    print("Homebrew로 uv 설치 완료")
                    return uv
            except subprocess.CalledProcessError:
                print("Homebrew 설치 실패. 공식 스크립트로 재시도합니다.")

        if platform.system() == "Windows":
            run(["powershell", "-ExecutionPolicy", "ByPass", "-c",
                 "irm https://astral.sh/uv/install.ps1 | iex"])
        else:
            # 타임아웃 설정 추가: 연결 10초, 전체 300초
            run(["sh", "-c", "curl -LsSf --connect-timeout 10 --max-time 300 https://astral.sh/uv/install.sh | sh"])
    except (subprocess.CalledProcessError, KeyboardInterrupt):
        print("\n\n!!! 공식 설치 스크립트 실행 중 오류가 발생했습니다 (네트워크 불안정 등).")
        print("pip를 통한 대체 설치를 시도합니다...")
        try:
            run([sys.executable, "-m", "pip", "install", "uv"])
        except subprocess.CalledProcessError:
            print("pip 설치도 실패했습니다.")

    # 설치 후 PATH에 추가 (현재 프로세스용)
    local_bin = os.path.join(os.path.expanduser("~"), ".local", "bin")
    cargo_bin = os.path.join(os.path.expanduser("~"), ".cargo", "bin")
    
    path_modified = False
    for p in [local_bin, cargo_bin]:
        if os.path.isdir(p) and p not in os.environ.get("PATH", ""):
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
            path_modified = True

    uv = shutil.which("uv")
    if not uv:
        # pip로 설치되었을 수도 있으므로 sys.executable 기반 bin 확인 등은 복잡하니 생략하고
        # PATH에 없을 경우 수동 설치 안내
        print("ERROR: uv 설치에 실패했습니다. 다음 방법들을 시도해보세요:")
        print("  1. 네트워크 연결 확인")
        print("  2. pip install uv (수동 실행)")
        print("  3. https://docs.astral.sh/uv/ 에서 바이너리 직접 다운로드")
        sys.exit(1)

    print("uv 설치 완료")
    if path_modified:
        print(f"NOTE: 'uv'가 {os.path.dirname(uv)}에 설치되었습니다. 터미널을 재시작하거나 PATH에 추가해주세요.")
        
    return uv


def check_venv() -> None:
    """venv의 Python 경로가 현재 디렉토리와 일치하는지 확인하고, 불일치 시 재생성한다."""
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

    print("기존 .venv의 Python 경로가 유효하지 않습니다. venv를 재생성합니다...")
    shutil.rmtree(venv_dir)
    print(".venv 삭제 완료")


def sync_dependencies(uv: str) -> None:
    check_venv()
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
            if not shutil.which("brew"):
                print("Error: Homebrew가 설치되어 있지 않습니다. https://brew.sh/ 에서 설치하세요.")
                return
            run(["brew", "install", "tesseract", "tesseract-lang"])
        elif system == "Linux":
            if not shutil.which("apt"):
                 print(f"Error: apt 패키지 관리자를 찾을 수 없습니다. 수동 설치가 필요합니다: {hint}")
                 return
            run(["sudo", "apt", "update"])
            run(["sudo", "apt", "install", "-y", "tesseract-ocr", "tesseract-ocr-kor"])
        elif system == "Windows":
            print(f"Windows에서는 수동 설치가 필요합니다: {hint}")
            return
        
        # 설치 확인
        if shutil.which("tesseract"):
             print("Tesseract 설치 완료")
        else:
             print("Warning: Tesseract 설치를 시도했으나 PATH에서 찾을 수 없습니다.")
    else:
        print("Tesseract 설치를 건너뜁니다. Google Vision API 키가 필요합니다.")


def run_tests(uv: str) -> bool:
    print("\n테스트를 실행합니다...")
    # uv run은 가상환경 내에서 실행하므로 python -m pytest 사용
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
        print("\n서버 실행: uv run fastmcp run src/handwriting_ocr_mcp/server.py:mcp")
    else:
        print("\n=== 설치 완료 (테스트 실패 항목이 있습니다) ===")


if __name__ == "__main__":
    main()
