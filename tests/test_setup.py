"""setup.py가 생성하는 Claude Desktop 설정이 올바른지 검증한다."""

from __future__ import annotations

import json
import os
import textwrap
from unittest.mock import patch

import pytest


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestConfigureClaudeDesktop:
    """configure_claude_desktop()가 절대경로로 서버를 등록하는지 확인."""

    def test_server_path_is_absolute(self, tmp_path):
        """생성된 설정의 서버 파일 경로가 절대경로인지 확인한다."""
        config_path = tmp_path / "claude_desktop_config.json"
        config_path.write_text("{}")

        with (
            patch("setup._get_claude_config_path", return_value=str(config_path)),
            patch("setup.sys") as mock_sys,
        ):
            mock_sys.stdin.isatty.return_value = False

            import setup

            setup.configure_claude_desktop("/usr/bin/uv")

        config = json.loads(config_path.read_text())
        server = config["mcpServers"]["handwriting-ocr-mcp"]
        # fastmcp run 뒤의 인자가 server.py 경로
        server_file_arg = server["args"][-1]  # "/.../server.py:mcp"
        path_part = server_file_arg.split(":")[0]

        assert os.path.isabs(path_part), f"서버 경로가 상대경로임: {path_part}"
        assert path_part.endswith("server.py")

    def test_server_path_points_to_real_file(self, tmp_path):
        """생성된 설정의 서버 파일이 실제로 존재하는지 확인한다."""
        config_path = tmp_path / "claude_desktop_config.json"
        config_path.write_text("{}")

        with (
            patch("setup._get_claude_config_path", return_value=str(config_path)),
            patch("setup.sys") as mock_sys,
        ):
            mock_sys.stdin.isatty.return_value = False

            import setup

            setup.configure_claude_desktop("/usr/bin/uv")

        config = json.loads(config_path.read_text())
        server_file_arg = config["mcpServers"]["handwriting-ocr-mcp"]["args"][-1]
        path_part = server_file_arg.split(":")[0]

        assert os.path.exists(path_part), f"서버 파일이 존재하지 않음: {path_part}"
