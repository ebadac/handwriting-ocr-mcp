
import os
import pytest
from unittest.mock import patch, MagicMock
from handwriting_ocr_mcp.server import ocr_image, _get_engine

def test_ocr_image_default_language(monkeypatch):
    # Mock engine
    mock_engine = MagicMock()
    mock_engine.extract_text.return_value = "text"
    
    with patch("handwriting_ocr_mcp.server._get_engine", return_value=mock_engine):
        # Case 1: No env var, no arg -> defaults to "en"
        monkeypatch.delenv("OCR_DEFAULT_LANGUAGE", raising=False)
        ocr_image.fn(image_data="AA==")
        mock_engine.extract_text.assert_called_with(image_data=b'\x00', lang="en")
        
        # Case 2: Env var set, no arg -> uses env var
        monkeypatch.setenv("OCR_DEFAULT_LANGUAGE", "ja")
        ocr_image.fn(image_data="AA==")
        mock_engine.extract_text.assert_called_with(image_data=b'\x00', lang="ja")
        
        # Case 3: Arg set -> overrides env var
        monkeypatch.setenv("OCR_DEFAULT_LANGUAGE", "ja")
        ocr_image.fn(image_data="AA==", lang="ko")
        mock_engine.extract_text.assert_called_with(image_data=b'\x00', lang="ko")

if __name__ == "__main__":
    # Manually run if executed directly
    from unittest.mock import MagicMock
    # ... logic to run with pytest ...
    import sys
    sys.exit(pytest.main(["-v", __file__]))
