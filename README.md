# handwriting-ocr-mcp

손글씨 이미지를 OCR로 텍스트 변환하는 MCP 서버입니다.
Google Cloud Vision API를 주 엔진으로, Tesseract를 폴백으로 지원합니다.

## 요구사항

- Python 3.10 이상
- [uv](https://docs.astral.sh/uv/) (패키지 매니저)
- Google Cloud Vision API 키 (선택) 또는 Tesseract OCR 바이너리 (폴백)
  - [Google Vision API 키 발급 가이드](docs/google_vision_setup.md)


## 빠른 설치

1. **설치 스크립트 실행**

   프로젝트 루트에서 다음 명령어를 실행하면, `uv` 설치부터 가상환경 구성, 의존성 설치, 그리고 **Google Cloud Credential 설정**까지 자동으로 진행됩니다.

   ```bash
   python3 setup.py
   ```

   > 스크립트 실행 중 Google Service Account JSON 키 파일의 경로를 묻습니다. 파일 경로를 입력하면 자동으로 프로젝트 내 `keys/` 디렉토리(git 무시됨)로 복사하고 `.env`를 설정해줍니다.

2. **OCR 테스트**

   설정이 완료되면 다음 스크립트로 동작을 확인할 수 있습니다.

   ```bash
   uv run scripts/verify_ocr.py
   ```

3. **수동 설치 (옵션)**

   자동 설치 스크립트를 사용하지 않을 경우:

   ```bash
   uv sync --extra tesseract
   cp .env.example .env
   # .env 파일에 GOOGLE_APPLICATION_CREDENTIALS 설정
   ```

### Tesseract 바이너리 설치 (폴백 사용 시)

| OS | 명령어 |
|----|--------|
| macOS | `brew install tesseract tesseract-lang` |
| Ubuntu/Debian | `sudo apt install tesseract-ocr tesseract-ocr-kor` |
| Windows | [UB-Mannheim 설치 프로그램](https://github.com/UB-Mannheim/tesseract/wiki) 다운로드 후 PATH에 추가 |

## 설정

`.env` 파일에 Google Cloud Service Account 키 파일 경로를 설정합니다:

```
GOOGLE_APPLICATION_CREDENTIALS="/path/to/project/keys/service-account.json"
```

- `GOOGLE_APPLICATION_CREDENTIALS`가 설정되어 있으면 Google Cloud Vision API를 사용합니다.
- 설정되어 있지 않거나 키가 유효하지 않으면 자동으로 Tesseract 폴백으로 전환됩니다. (Tesseract 설치 필요)

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
      "args": ["run", "--project", "/absolute/path/to/handwriting-ocr-mcp", "fastmcp", "run", "src/handwriting_ocr_mcp/server.py:mcp"]
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
