from __future__ import annotations

from unittest.mock import MagicMock, patch

from handwriting_ocr_mcp.ocr.base import create_engine


class TestCreateEngine:
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
    @patch("handwriting_ocr_mcp.ocr.google_vision.GoogleVisionEngine")
    def test_creates_google_engine_when_api_key_set(self, mock_cls: MagicMock) -> None:
        engine = create_engine()
        mock_cls.assert_called_once()
        assert engine is mock_cls.return_value

    @patch.dict("os.environ", {}, clear=True)
    @patch("handwriting_ocr_mcp.ocr.tesseract.TesseractEngine")
    def test_creates_tesseract_engine_when_no_api_key(self, mock_cls: MagicMock) -> None:
        engine = create_engine()
        mock_cls.assert_called_once()
        assert engine is mock_cls.return_value


class TestTesseractEngine:
    @patch("handwriting_ocr_mcp.ocr.tesseract.pytesseract")
    @patch("handwriting_ocr_mcp.ocr.tesseract.Image")
    def test_extract_text(self, mock_image: MagicMock, mock_pytesseract: MagicMock) -> None:
        mock_pytesseract.image_to_string.return_value = "안녕하세요\n"

        from handwriting_ocr_mcp.ocr.tesseract import TesseractEngine

        engine = TesseractEngine()
        result = engine.extract_text("/fake/path.png", lang="ko")

        mock_image.open.assert_called_once_with("/fake/path.png")
        mock_pytesseract.image_to_string.assert_called_once_with(
            mock_image.open.return_value, lang="kor"
        )
        assert result == "안녕하세요"

    @patch("handwriting_ocr_mcp.ocr.tesseract.pytesseract")
    def test_supported_languages(self, _mock: MagicMock) -> None:
        from handwriting_ocr_mcp.ocr.tesseract import TesseractEngine

        engine = TesseractEngine()
        langs = engine.supported_languages()
        assert "ko" in langs
        assert "en" in langs
