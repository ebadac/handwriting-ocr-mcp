"""MCP 서버가 임의의 cwd에서 정상 기동되는지 검증한다."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_PATH = os.path.join(
    PROJECT_ROOT, "src", "handwriting_ocr_mcp", "server.py"
)
UV = "uv"


def _run_mcp_request(request: dict, cwd: str = "/") -> dict:
    """MCP 서버에 JSON-RPC 요청을 보내고 응답을 반환한다."""
    # stdin으로 JSON-RPC 요청을 보내고 stdout에서 응답을 받는다
    input_line = json.dumps(request)
    result = subprocess.run(
        [
            UV, "run",
            "--project", PROJECT_ROOT,
            "fastmcp", "run",
            f"{SERVER_PATH}:mcp",
        ],
        input=input_line + "\n",
        capture_output=True,
        text=True,
        timeout=30,
        cwd=cwd,
    )
    return result


class TestServerStartup:
    """서버가 프로젝트 디렉토리가 아닌 곳에서도 기동되는지 확인."""

    def test_server_starts_from_root_directory(self, tmp_path):
        """cwd가 /tmp 일 때도 서버가 파일을 찾을 수 있는지 확인한다."""
        result = subprocess.run(
            [
                UV, "run",
                "--project", PROJECT_ROOT,
                "fastmcp", "run",
                f"{SERVER_PATH}:mcp",
            ],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(tmp_path),  # 프로젝트 밖의 임의 디렉토리
        )
        # "File not found" 에러가 없어야 한다
        assert "File not found" not in result.stderr, (
            f"서버가 파일을 찾지 못함 (cwd={tmp_path}):\n{result.stderr}"
        )

    def test_server_starts_from_home_directory(self):
        """cwd가 홈 디렉토리일 때도 서버가 기동되는지 확인한다."""
        home = os.path.expanduser("~")
        result = subprocess.run(
            [
                UV, "run",
                "--project", PROJECT_ROOT,
                "fastmcp", "run",
                f"{SERVER_PATH}:mcp",
            ],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
            cwd=home,
        )
        assert "File not found" not in result.stderr, (
            f"서버가 파일을 찾지 못함 (cwd={home}):\n{result.stderr}"
        )
