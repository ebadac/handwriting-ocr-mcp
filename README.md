# handwriting-ocr-mcp

손글씨 이미지를 OCR로 텍스트 변환하는 MCP 서버입니다.
Google Cloud Vision API를 주 엔진으로, Tesseract를 폴백으로 지원합니다.

## 요구사항

- Python 3.10 이상
- [uv](https://docs.astral.sh/uv/) (패키지 매니저)
- Google Cloud Vision API 키 (선택) 또는 Tesseract OCR 바이너리 (폴백)

## 설치

```bash
git clone git@github.com:ebadac/handwriting-ocr-mcp.git
cd handwriting-ocr-mcp
uv sync
```

Tesseract 폴백을 사용하려면 추가 의존성을 설치합니다:

```bash
uv sync --extra tesseract
```

### Tesseract 바이너리 설치 (폴백 사용 시)

macOS:

```bash
brew install tesseract tesseract-lang
```

Ubuntu/Debian:

```bash
sudo apt install tesseract-ocr tesseract-ocr-kor
```

## 설정

`.env.example`을 복사하여 `.env` 파일을 생성합니다:

```bash
cp .env.example .env
```

`.env` 파일에 Google Cloud Vision API 키를 설정합니다:

```
GOOGLE_API_KEY=your-api-key-here
```

- `GOOGLE_API_KEY`가 설정되어 있으면 Google Cloud Vision API를 사용합니다.
- 설정되어 있지 않으면 자동으로 Tesseract 폴백으로 전환됩니다.

## 사용법

### MCP 서버 실행

```bash
fastmcp run src/handwriting_ocr_mcp/server.py:mcp
```

### Claude Desktop에서 사용

`claude_desktop_config.json`에 다음을 추가합니다:

```json
{
  "mcpServers": {
    "handwriting-ocr-mcp": {
      "command": "fastmcp",
      "args": ["run", "/absolute/path/to/handwriting-ocr-mcp/src/handwriting_ocr_mcp/server.py:mcp"],
      "env": {
        "GOOGLE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### 제공 도구

#### `ocr_image`

손글씨 이미지에서 텍스트를 추출합니다.

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|-------|------|
| `image_path` | `str` | (필수) | OCR을 수행할 이미지 파일 경로 |
| `lang` | `str` | `"ko"` | OCR 언어 코드 |

#### `list_supported_languages`

지원하는 OCR 언어 목록을 반환합니다. 파라미터 없음.

### 지원 언어

| 코드 | 언어 |
|------|------|
| `ko` | 한국어 |
| `en` | 영어 |
| `ja` | 일본어 |
| `zh` | 중국어 (간체) |
| `zh-TW` | 중국어 (번체) |
| `de` | 독일어 |
| `fr` | 프랑스어 |
| `es` | 스페인어 |
| `it` | 이탈리아어 |
| `pt` | 포르투갈어 |
| `ru` | 러시아어 |

## 개발

```bash
# 개발 의존성 포함 설치
uv sync --extra dev --extra tesseract

# 테스트 실행
pytest tests/

# 린트
ruff check src/ tests/
```
