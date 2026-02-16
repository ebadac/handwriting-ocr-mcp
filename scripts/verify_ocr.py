
import os
import sys
from dotenv import load_dotenv

# Calculate project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(project_root, ".env"))

# Add src to path
sys.path.append(os.path.join(project_root, "src"))

from handwriting_ocr_mcp.server import _get_engine

try:
    print("Initialize OCR engine...")
    engine = _get_engine()
    print("Running OCR on tests/test.png...")
    # absolute path to be safe
    image_path = os.path.join(project_root, "tests", "test.png")
    result = engine.extract_text(image_path=image_path, lang="ko")
    print("OCR Result:")
    print(result)
except Exception as e:
    print(f"Error: {e}")
