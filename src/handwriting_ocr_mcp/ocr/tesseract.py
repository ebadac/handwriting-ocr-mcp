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
                "pytesseract is not installed. "
                "Install it with `pip install 'handwriting-ocr-mcp[tesseract]'`."
            )

    def extract_text(
        self,
        image_path: str | None = None,
        lang: str = "en",
        *,
        image_data: bytes | None = None,
    ) -> str:
        """Extracts text from the image using Tesseract OCR."""
        tess_lang = LANG_MAP.get(lang, lang)
        if image_data is not None:
            image = Image.open(io.BytesIO(image_data))
        elif image_path is not None:
            image = Image.open(image_path)
        else:
            raise ValueError("Either image_path or image_data must be provided.")
        text: str = pytesseract.image_to_string(image, lang=tess_lang)
        return text.strip()

    def supported_languages(self) -> list[str]:
        return list(LANG_MAP.keys())
