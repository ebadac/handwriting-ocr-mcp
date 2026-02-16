from __future__ import annotations

try:
    import pytesseract
except ImportError:
    pytesseract = None  # type: ignore[assignment]

import io

from PIL import Image


LANG_MAP: dict[str, str] = {
    "ko": "kor",
    "en": "eng",
    "ja": "jpn",
    "zh": "chi_sim",
    "zh-TW": "chi_tra",
    "de": "deu",
    "fr": "fra",
    "es": "spa",
    "it": "ita",
    "pt": "por",
    "ru": "rus",
}


class TesseractEngine:
    def __init__(self) -> None:
        if pytesseract is None:
            raise RuntimeError(
                "pytesseract가 설치되지 않았습니다. "
                "`pip install 'handwriting-ocr-mcp[tesseract]'`로 설치하세요."
            )

    def extract_text(
        self,
        image_path: str | None = None,
        lang: str = "ko",
        *,
        image_data: bytes | None = None,
    ) -> str:
        """Tesseract OCR로 이미지에서 텍스트를 추출합니다."""
        tess_lang = LANG_MAP.get(lang, lang)
        if image_data is not None:
            image = Image.open(io.BytesIO(image_data))
        elif image_path is not None:
            image = Image.open(image_path)
        else:
            raise ValueError("image_path 또는 image_data 중 하나를 제공해야 합니다.")
        text: str = pytesseract.image_to_string(image, lang=tess_lang)
        return text.strip()

    def supported_languages(self) -> list[str]:
        return list(LANG_MAP.keys())
