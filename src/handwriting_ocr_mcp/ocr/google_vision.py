from __future__ import annotations

import os

from google.cloud import vision


class GoogleVisionEngine:
    SUPPORTED_LANGUAGES = [
        "ko", "en", "ja", "zh", "zh-TW", "de", "fr", "es", "it", "pt", "ru",
    ]


    def __init__(self) -> None:
        # Check for Service Account (preferred)
        self._service_account_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self._api_key = os.environ.get("GOOGLE_API_KEY")

        if self._service_account_path:
             # Client library automatically uses GOOGLE_APPLICATION_CREDENTIALS if set
            self._client = vision.ImageAnnotatorClient()
        elif self._api_key:
             # Fallback to API Key
            self._client = vision.ImageAnnotatorClient(
                client_options={"api_key": self._api_key},
            )
        else:
            raise RuntimeError(
                "Google Cloud Vision 인증 정보가 설정되지 않았습니다.\n"
                "GOOGLE_APPLICATION_CREDENTIALS(서비스 계정 키 파일 경로) 또는 "
                "GOOGLE_API_KEY 환경변수를 설정해주세요."
            )

    def extract_text(
        self,
        image_path: str | None = None,
        lang: str = "ko",
        *,
        image_data: bytes | None = None,
    ) -> str:
        """Google Cloud Vision API로 이미지에서 텍스트를 추출합니다."""
        if image_data is not None:
            content = image_data
        elif image_path is not None:
            with open(image_path, "rb") as f:
                content = f.read()
        else:
            raise ValueError("image_path 또는 image_data 중 하나를 제공해야 합니다.")

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
