from __future__ import annotations

from fastmcp import FastMCP

from handwriting_ocr_mcp.ocr.base import OcrEngine, create_engine

mcp = FastMCP("handwriting-ocr-mcp")

_engine: OcrEngine | None = None


def _get_engine() -> OcrEngine:
    global _engine
    if _engine is None:
        _engine = create_engine()
    return _engine


@mcp.tool()
def ocr_image(image_path: str, lang: str = "ko") -> str:
    """손글씨 이미지에서 텍스트를 추출합니다.

    Args:
        image_path: OCR을 수행할 이미지 파일 경로
        lang: OCR 언어 코드 (기본값: ko)

    Returns:
        추출된 텍스트
    """
    engine = _get_engine()
    return engine.extract_text(image_path, lang=lang)


@mcp.tool()
def list_supported_languages() -> list[str]:
    """지원하는 OCR 언어 목록을 반환합니다."""
    engine = _get_engine()
    return engine.supported_languages()
