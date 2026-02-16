# handwriting-ocr-mcp

손글씨 이미지를 OCR로 텍스트 변환하는 MCP 서버입니다.
Google Cloud Vision API를 주 엔진으로, Tesseract를 폴백으로 지원합니다.

## 요구사항

- Python 3.10 이상
- [uv](https://docs.astral.sh/uv/) (패키지 매니저)
- Google Cloud Vision API 키 (선택) 또는 Tesseract OCR 바이너리 (폴백)

## 빠른 설치

설치 스크립트가 uv, 의존성, .env 파일, Tesseract 설치를 자동으로 처리합니다.

```bash
git clone git@github.com:ebadac/handwriting-ocr-mcp.git
cd handwriting-ocr-mcp
python3 setup.py
```

Windows:

```powershell
git clone git@github.com:ebadac/handwriting-ocr-mcp.git
cd handwriting-ocr-mcp
python setup.py
```

## 수동 설치

```bash
uv sync --extra tesseract
cp .env.example .env
```

### Tesseract 바이너리 설치 (폴백 사용 시)

| OS | 명령어 |
|----|--------|
| macOS | `brew install tesseract tesseract-lang` |
| Ubuntu/Debian | `sudo apt install tesseract-ocr tesseract-ocr-kor` |
| Windows | [UB-Mannheim 설치 프로그램](https://github.com/UB-Mannheim/tesseract/wiki) 다운로드 후 PATH에 추가 |

## 설정

`.env` 파일에 Google Cloud Vision API 키를 설정합니다:

```
GOOGLE_API_KEY=your-api-key-here
```

- `GOOGLE_API_KEY`가 설정되어 있으면 Google Cloud Vision API를 사용합니다.
- 설정되어 있지 않으면 자동으로 Tesseract 폴백으로 전환됩니다.

## 사용법

### MCP 서버 실행

```bash
uv run fastmcp run src/handwriting_ocr_mcp/server.py:mcp
```

### Claude Desktop에서 사용

`claude_desktop_config.json`에 다음을 추가합니다:
> setup.py에 의해 자동으로 설정됩니다.

```json
{
  "mcpServers": {
    "handwriting-ocr-mcp": {
      "command": "uv",
      "args": ["run", "--project", "/absolute/path/to/handwriting-ocr-mcp", "fastmcp", "run", "src/handwriting_ocr_mcp/server.py:mcp"],
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
| `image_path` | `str \| None` | `None` | OCR을 수행할 이미지 파일 경로 (image_data와 둘 중 하나 필수) |
| `image_data` | `str \| None` | `None` | base64 인코딩된 이미지 데이터 (image_path와 둘 중 하나 필수) |
| `lang` | `str` | `"ko"` | OCR 언어 코드 |

#### `list_supported_languages`

지원하는 OCR 언어 목록을 반환합니다. 파라미터 없음.

### 사용 예시

#### 파일 경로로 호출

```python
# MCP 클라이언트에서
result = ocr_image(image_path="/path/to/business_card.jpg", lang="ko")
```

#### Claude Desktop에서 사용

Claude Desktop에서 이미지를 업로드한 경우:
1. **권장**: 이미지를 로컬에 저장 후 절대 경로를 MCP 도구에 전달
2. **대안**: Claude가 이미지를 base64로 인코딩하여 전달 (토큰 소모 주의)

**중요**: MCP 서버는 Claude가 업로드한 임시 파일에 직접 접근할 수 없습니다.
파일을 특정 위치에 저장하고 그 경로를 제공해야 합니다.

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
uv run python -m pytest tests/

# 린트
uv run ruff check src/ tests/
```
