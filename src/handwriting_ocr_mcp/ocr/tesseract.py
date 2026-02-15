from __future__ import annotations

try:
    import pytesseract
except ImportError:
    pytesseract = None  # type: ignore[assignment]

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

    def extract_text(self, image_path: str, lang: str = "ko") -> str:
        """Tesseract OCR로 이미지에서 텍스트를 추출합니다."""
        tess_lang = LANG_MAP.get(lang, lang)
        image = Image.open(image_path)
        text: str = pytesseract.image_to_string(image, lang=tess_lang)
        return text.strip()

    def supported_languages(self) -> list[str]:
        return list(LANG_MAP.keys())
