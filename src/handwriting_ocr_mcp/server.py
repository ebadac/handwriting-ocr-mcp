from __future__ import annotations

import base64

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
def ocr_image(
    image_path: str | None = None,
    lang: str = "ko",
    image_data: str | None = None,
) -> str:
    """Extracts text from handwriting image.

    Args:
        image_path: Image file path for OCR
        lang: OCR language code (default: ko)
        image_data: Base64 encoded image data (can be used instead of image_path)

    Returns:
        Extracted text
    """
    engine = _get_engine()
    if image_data is not None:
        raw = base64.b64decode(image_data)
        return engine.extract_text(image_data=raw, lang=lang)
    if image_path is not None:
        return engine.extract_text(image_path=image_path, lang=lang)
    raise ValueError(
        "Either image_path or image_data must be provided.\n"
        "Examples:\n"
        "  - image_path: '/path/to/image.png'\n"
        "  - image_data: base64 encoded string"
    )


@mcp.tool()
def list_supported_languages() -> list[str]:
    """Returns list of supported OCR languages."""
    engine = _get_engine()
    return engine.supported_languages()
