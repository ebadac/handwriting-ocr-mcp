#!/usr/bin/env bash
set -euo pipefail

echo "=== handwriting-ocr-mcp 설치 ==="

# uv 설치 확인
if ! command -v uv &> /dev/null; then
    echo "uv가 설치되어 있지 않습니다. 설치합니다..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "uv 설치 완료"
fi

echo "uv version: $(uv --version)"

# 의존성 설치
echo ""
echo "의존성을 설치합니다..."
uv sync --extra dev --extra tesseract
echo "의존성 설치 완료"

# .env 파일 생성
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo ".env 파일이 생성되었습니다."
    echo "Google Vision API를 사용하려면 .env 파일에 GOOGLE_API_KEY를 설정하세요."
fi

# Tesseract 바이너리 설치 (폴백용)
if ! command -v tesseract &> /dev/null; then
    echo ""
    echo "Tesseract OCR이 설치되어 있지 않습니다."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        read -rp "Homebrew로 Tesseract를 설치할까요? (y/N) " answer
        if [[ "$answer" =~ ^[yY]$ ]]; then
            brew install tesseract tesseract-lang
            echo "Tesseract 설치 완료"
        else
            echo "Tesseract 설치를 건너뜁니다. Google Vision API 키가 필요합니다."
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        read -rp "apt로 Tesseract를 설치할까요? (y/N) " answer
        if [[ "$answer" =~ ^[yY]$ ]]; then
            sudo apt install -y tesseract-ocr tesseract-ocr-kor
            echo "Tesseract 설치 완료"
        else
            echo "Tesseract 설치를 건너뜁니다. Google Vision API 키가 필요합니다."
        fi
    else
        echo "자동 설치를 지원하지 않는 OS입니다. 수동으로 Tesseract를 설치하세요."
    fi
else
    echo "Tesseract: $(tesseract --version 2>&1 | head -1)"
fi

# 테스트 실행
echo ""
echo "테스트를 실행합니다..."
if uv run pytest tests/ -q; then
    echo ""
    echo "=== 설치 완료 ==="
    echo ""
    echo "서버 실행: fastmcp run src/handwriting_ocr_mcp/server.py:mcp"
else
    echo ""
    echo "=== 설치 완료 (테스트 실패 항목이 있습니다) ==="
fi
