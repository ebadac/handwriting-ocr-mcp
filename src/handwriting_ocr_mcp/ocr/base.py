from __future__ import annotations

import os
from typing import Protocol


class OcrEngine(Protocol):
    def extract_text(
        self,
        image_path: str | None = None,
        lang: str = "en",
        *,
        image_data: bytes | None = None,
    ) -> str:
        """Extracts text from the image.

        Either image_path or image_data must be provided.
        """
        ...

    def supported_languages(self) -> list[str]:
        """Returns the list of supported languages."""
        ...


def create_engine() -> OcrEngine:
    """Selects an OCR engine based on environment variables.

    If GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_API_KEY is set, Google Vision is used.
    Otherwise, Tesseract is used.
    """
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.environ.get("GOOGLE_API_KEY"):
        from handwriting_ocr_mcp.ocr.google_vision import GoogleVisionEngine

        return GoogleVisionEngine()

    from handwriting_ocr_mcp.ocr.tesseract import TesseractEngine

    return TesseractEngine()
