# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**handwriting-ocr-mcp** — MCP server based on Python + FastMCP. Provides tools to convert handwriting images to text using OCR.
Supports Google Vision API as the primary engine and Tesseract as a fallback.

## Repository

- Remote: git@github.com:ebadac/handwriting-ocr-mcp.git
- Main branch: `main`

## Build & Run

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev --extra tesseract

# Run MCP server
uv run fastmcp run src/handwriting_ocr_mcp/server.py:mcp

# Run tests
uv run python -m pytest tests/

# Lint
uv run ruff check src/ tests/
```

## Architecture

- `src/handwriting_ocr_mcp/server.py` — FastMCP server, MCP tool registration
- `src/handwriting_ocr_mcp/ocr/base.py` — OcrEngine Protocol + Factory function
- `src/handwriting_ocr_mcp/ocr/google_vision.py` — Google Cloud Vision implementation
- `src/handwriting_ocr_mcp/ocr/tesseract.py` — Tesseract fallback implementation

## Environment Variables

- `GOOGLE_API_KEY` — Google Cloud Vision API key (Uses Google Vision if set, falls back to Tesseract if not set)
