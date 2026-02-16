from __future__ import annotations

import base64
import os

from dotenv import load_dotenv
from fastmcp import FastMCP

from handwriting_ocr_mcp.ocr.base import OcrEngine, create_engine

# Load environment variables from .env file
load_dotenv()



mcp = FastMCP("handwriting-ocr-mcp")

_engine: OcrEngine | None = None


def _get_engine() -> OcrEngine:
    global _engine
    if _engine is None:
        _engine = create_engine()
    return _engine


@mcp.tool(
    name="ocr_image",
    description="Extracts text from a handwriting image file or base64 data. Supports multiple languages (default: Korean).",
)
def ocr_image(
    image_path: str | None = None,
    lang: str = "ko",
    image_data: str | None = None,
) -> str:
    """Extracts text from handwriting image.

    Args:
        image_path: Absolute path to the local image file to perform OCR on.
        lang: Language code for OCR (e.g., 'ko' for Korean, 'en' for English). Defaults to 'ko'.
        image_data: Base64 encoded string of the image data. Use this if the image is not stored locally.

    Returns:
        The extracted text as a string.

    Raises:
        ValueError: If neither image_path nor image_data is provided.
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


@mcp.tool(
    name="list_supported_languages",
    description="Returns a list of supported language codes for the OCR tool.",
)
def list_supported_languages() -> list[str]:
    """Returns list of supported OCR languages.

    Returns:
        A list of string language codes (e.g., ['ko', 'en', ...]) supported by the current OCR engine.
    """
    engine = _get_engine()
    return engine.supported_languages()
