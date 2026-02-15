# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**handwriting-ocr-mcp** — Python + FastMCP 기반 MCP 서버. 손글씨 이미지를 OCR로 텍스트 변환하는 도구를 제공한다.
Google Vision API를 주 엔진으로, Tesseract를 폴백으로 지원.

## Repository

- Remote: git@github.com:ebadac/handwriting-ocr-mcp.git
- Main branch: `main`

## Build & Run

```bash
# 의존성 설치
uv sync

# 개발 의존성 포함 설치
uv sync --extra dev --extra tesseract

# MCP 서버 실행
uv run fastmcp run src/handwriting_ocr_mcp/server.py:mcp

# 테스트 실행
uv run python -m pytest tests/

# 린트
uv run ruff check src/ tests/
```

## Architecture

- `src/handwriting_ocr_mcp/server.py` — FastMCP 서버, MCP 도구 등록
- `src/handwriting_ocr_mcp/ocr/base.py` — OcrEngine Protocol + 팩토리 함수
- `src/handwriting_ocr_mcp/ocr/google_vision.py` — Google Cloud Vision 구현
- `src/handwriting_ocr_mcp/ocr/tesseract.py` — Tesseract 폴백 구현

## Environment Variables

- `GOOGLE_API_KEY` — Google Cloud Vision API 키 (설정 시 Google Vision 사용, 미설정 시 Tesseract 폴백)
