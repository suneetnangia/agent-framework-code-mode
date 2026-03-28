# Copyright (c) Microsoft. All rights reserved.

"""Inline script runner for dynamically generated Python code.

Executes LLM-generated Python code in an isolated subprocess via a temporary file.
This is provided for demonstration purposes only.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

MAX_CODE_SIZE = 10_240  # 10 KB
EXECUTION_TIMEOUT = 60  # seconds
MAX_OUTPUT_SIZE = 50_000  # characters


def inline_script_runner(code: str) -> str:
    """Run dynamically generated Python code in a subprocess.

    Writes the code to a temporary file, executes it with the current
    Python interpreter, and returns captured output.

    Args:
        code: The Python source code to execute.

    Returns:
        The combined stdout/stderr output, or an error message.
    """
    if not code or not code.strip():
        return "Error: No code provided."

    if len(code) > MAX_CODE_SIZE:
        return f"Error: Code exceeds maximum size of {MAX_CODE_SIZE} bytes."

    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix="inline_",
            delete=False,
        )
        tmp_file.write(code)
        tmp_file.close()

        # Run with minimal environment to avoid leaking secrets
        safe_env = {
            # Minimal PATH; sys.executable is invoked by absolute path
            "PATH": "/usr/bin:/bin",
            # Temp dir instead of real home to prevent reading .ssh, .azure, etc.
            "HOME": tempfile.gettempdir(),
            # Empty to prevent importing from the host project
            "PYTHONPATH": "",
            # Block loading packages from ~/.local/lib/pythonX.Y/site-packages
            "PYTHONNOUSERSITE": "1",
            # Prevent .pyc file creation outside the sandbox
            "PYTHONDONTWRITEBYTECODE": "1",
            # Prevent unsafe sys.path manipulation via script directory
            "PYTHONSAFEPATH": "1",
            # Predictable encoding behaviour
            "LC_ALL": "C.UTF-8",
        }

        result = subprocess.run(
            [sys.executable, tmp_file.name],
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT,
            cwd=tempfile.gettempdir(),
            env=safe_env,
        )

        output = result.stdout
        if result.stderr:
            output += f"\nStderr:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nScript exited with code {result.returncode}"

        # Truncate output to prevent excessive memory usage
        if len(output) > MAX_OUTPUT_SIZE:
            output = output[:MAX_OUTPUT_SIZE] + "\n... (output truncated)"

        return output.strip() or "(no output)"

    except subprocess.TimeoutExpired:
        return f"Error: Code execution timed out after {EXECUTION_TIMEOUT} seconds."
    except OSError as e:
        return f"Error: Failed to execute code: {e}"
    finally:
        if tmp_file is not None:
            Path(tmp_file.name).unlink(missing_ok=True)
