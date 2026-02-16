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
                "Google Cloud Vision credentials are not set.\n"
                "Please set GOOGLE_APPLICATION_CREDENTIALS (path to service account key file) "
                "or GOOGLE_API_KEY environment variable."
            )

    def extract_text(
        self,
        image_path: str | None = None,
        lang: str = "en",
        *,
        image_data: bytes | None = None,
    ) -> str:
        """Extracts text from the image using Google Cloud Vision API."""
        if image_data is not None:
            content = image_data
        elif image_path is not None:
            with open(image_path, "rb") as f:
                content = f.read()
        else:
            raise ValueError("Either image_path or image_data must be provided.")

        image = vision.Image(content=content)
        image_context = vision.ImageContext(
            language_hints=[lang],
        )
        response = self._client.document_text_detection(
            image=image,
            image_context=image_context,
        )

        if response.error.message:
            raise RuntimeError(f"Vision API Error: {response.error.message}")

        if not response.full_text_annotation:
            return ""

        return response.full_text_annotation.text

    def supported_languages(self) -> list[str]:
        return self.SUPPORTED_LANGUAGES
