from __future__ import annotations

import os
from typing import Protocol


class OcrEngine(Protocol):
    def extract_text(self, image_path: str, lang: str = "ko") -> str:
        """이미지에서 텍스트를 추출합니다."""
        ...

    def supported_languages(self) -> list[str]:
        """지원하는 언어 목록을 반환합니다."""
        ...


def create_engine() -> OcrEngine:
    """환경변수 기반으로 OCR 엔진을 선택합니다.

    GOOGLE_API_KEY가 설정되어 있으면 Google Vision, 아니면 Tesseract를 사용합니다.
    """
    if os.environ.get("GOOGLE_API_KEY"):
        from handwriting_ocr_mcp.ocr.google_vision import GoogleVisionEngine

        return GoogleVisionEngine()

    from handwriting_ocr_mcp.ocr.tesseract import TesseractEngine

    return TesseractEngine()
