"""Verifies that the MCP server starts correctly from an arbitrary cwd."""

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
    """Sends a JSON-RPC request to the MCP server and returns the response."""
    # Send JSON-RPC request to stdin and receive response from stdout
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
    """Check if the server starts even from outside the project directory."""

    def test_server_starts_from_root_directory(self, tmp_path):
        """Checks if the server can find files even when cwd is /tmp."""
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
            cwd=str(tmp_path),  # Arbitrary directory outside the project
        )
        # Should not have "File not found" error
        assert "File not found" not in result.stderr, (
            f"Server failed to find files (cwd={tmp_path}):\n{result.stderr}"
        )

    def test_server_starts_from_home_directory(self):
        """Checks if the server starts when cwd is the home directory."""
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
            f"Server failed to find files (cwd={home}):\n{result.stderr}"
        )
