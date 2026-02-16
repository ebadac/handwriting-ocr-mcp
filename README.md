# handwriting-ocr-mcp

An MCP server that converts handwriting images to text using OCR.
It supports Google Cloud Vision API as the primary engine and Tesseract as a fallback.

## Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (Package Manager)
- Google Cloud Vision API key (Optional) or Tesseract OCR binary (Fallback)
  - [Google Vision API Key Setup Guide](docs/google_vision_setup.md)


## Quick Installation

1. **Run Installation Script**

   Run the following command in the project root to automatically install `uv`, configure the virtual environment, install dependencies, and **set up Google Cloud Credentials**.

   ```bash
   python3 setup.py
   ```

   > During script execution, you will be asked for the path to your Google Service Account JSON key file. If provided, it will be automatically copied to the `keys/` directory (ignored by git) in the project, and `.env` will be configured.

2. **Test OCR**

   Once configured, you can verify the operation with the following script:

   ```bash
   uv run scripts/verify_ocr.py
   ```

3. **Manual Installation (Optional)**

   If you do not use the automatic installation script:

   ```bash
   uv sync --extra tesseract
   cp .env.example .env
   # Set GOOGLE_APPLICATION_CREDENTIALS in .env file
   ```

### Install Tesseract Binary (If using fallback)

| OS | Command |
|----|---------|
| macOS | `brew install tesseract tesseract-lang` |
| Ubuntu/Debian | `sudo apt install tesseract-ocr tesseract-ocr-kor` |
| Windows | Download [UB-Mannheim Installer](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH |

## Configuration

Set the path to your Google Cloud Service Account key file in the `.env` file:

```
GOOGLE_APPLICATION_CREDENTIALS="/path/to/project/keys/service-account.json"
```

- If `GOOGLE_APPLICATION_CREDENTIALS` is set, Google Cloud Vision API is used.
- If not set or the key is invalid, it automatically falls back to Tesseract (Tesseract installation required).

## Usage

### Run MCP Server

```bash
uv run fastmcp run src/handwriting_ocr_mcp/server.py:mcp
```

### Use in Claude Desktop

Add the following to `claude_desktop_config.json`:
> This is automatically configured by setup.py.

```json
{
  "mcpServers": {
    "handwriting-ocr-mcp": {
      "command": "uv",
      "args": ["run", "--project", "/absolute/path/to/handwriting-ocr-mcp", "fastmcp", "run", "src/handwriting_ocr_mcp/server.py:mcp"]
    }
  }
}
```

### Available Tools

#### `ocr_image`

Extracts text from a handwriting image.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image_path` | `str \| None` | `None` | Path to the image file for OCR (Required if image_data is not provided) |
| `image_data` | `str \| None` | `None` | Base64 encoded image data (Required if image_path is not provided) |
| `lang` | `str` | `"en"` | OCR Language Code |

#### `list_supported_languages`

Returns a list of supported OCR languages. No parameters.

### Usage Examples

#### Call with File Path

```python
# In MCP Client
result = ocr_image(image_path="/path/to/business_card.jpg", lang="en")
```

#### Use in Claude Desktop

When uploading an image in Claude Desktop:
1. **Recommended**: Save the image locally and provide the absolute path to the MCP tool.
2. **Alternative**: Claude encodes the image to base64 and passes it (Note: token consumption).

**Important**: The MCP server cannot directly access temporary files uploaded by Claude.
You must save the file to a specific location and provide that path.

### Supported Languages

| Code | Language |
|------|----------|
| `ko` | Korean |
| `en` | English |
| `ja` | Japanese |
| `zh` | Chinese (Simplified) |
| `zh-TW` | Chinese (Traditional) |
| `de` | German |
| `fr` | French |
| `es` | Spanish |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |

## Development

```bash
# Install with dev dependencies
uv sync --extra dev --extra tesseract

# Run tests
uv run python -m pytest tests/

# Lint
uv run ruff check src/ tests/
```
