from __future__ import annotations

import os

from google.cloud import vision


class GoogleVisionEngine:
    SUPPORTED_LANGUAGES = [
        "ko", "en", "ja", "zh", "zh-TW", "de", "fr", "es", "it", "pt", "ru",
    ]

    def __init__(self) -> None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        self._client = vision.ImageAnnotatorClient(
            client_options={"api_key": api_key},
        )

    def extract_text(self, image_path: str, lang: str = "ko") -> str:
        """Google Cloud Vision API로 이미지에서 텍스트를 추출합니다."""
        with open(image_path, "rb") as f:
            content = f.read()

        image = vision.Image(content=content)
        image_context = vision.ImageContext(
            language_hints=[lang],
        )
        response = self._client.document_text_detection(
            image=image,
            image_context=image_context,
        )

        if response.error.message:
            raise RuntimeError(f"Vision API 오류: {response.error.message}")

        if not response.full_text_annotation:
            return ""

        return response.full_text_annotation.text

    def supported_languages(self) -> list[str]:
        return self.SUPPORTED_LANGUAGES
