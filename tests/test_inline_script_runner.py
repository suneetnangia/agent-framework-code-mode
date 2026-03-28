import os

# The orchestrator __init__.py reads Azure env vars at import time,
# so set dummy values before importing the runner module.
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com")
os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT_NAME", "test-deployment")

from progressive_exposure.agents.orchestrator.subprocess_inline_script_runner import (  # noqa: E402
    MAX_CODE_SIZE,
    inline_script_runner,
)


class TestInlineScriptRunner:
    def test_simple_print(self) -> None:
        result = inline_script_runner('print("hello")')
        assert result == "hello"

    def test_computation(self) -> None:
        result = inline_script_runner("print(2 + 2)")
        assert result == "4"

    def test_multiline_code(self) -> None:
        code = "x = 3\ny = 7\nprint(x * y)"
        result = inline_script_runner(code)
        assert result == "21"

    def test_empty_code(self) -> None:
        result = inline_script_runner("")
        assert result == "Error: No code provided."

    def test_whitespace_only_code(self) -> None:
        result = inline_script_runner("   \n  ")
        assert result == "Error: No code provided."

    def test_code_exceeds_max_size(self) -> None:
        code = "x = 1\n" * (MAX_CODE_SIZE + 1)
        result = inline_script_runner(code)
        assert "exceeds maximum size" in result

    def test_syntax_error(self) -> None:
        result = inline_script_runner("def foo(")
        assert "Stderr:" in result
        assert "Script exited with code 1" in result

    def test_runtime_error(self) -> None:
        result = inline_script_runner("raise ValueError('test error')")
        assert "ValueError" in result
        assert "test error" in result

    def test_no_output(self) -> None:
        result = inline_script_runner("x = 42")
        assert result == "(no output)"

    def test_no_env_leakage(self) -> None:
        code = 'import os\nprint(os.environ.get("AZURE_OPENAI_ENDPOINT", "NOT_FOUND"))'
        result = inline_script_runner(code)
        assert result == "NOT_FOUND"

    def test_temp_file_cleaned_up(self) -> None:
        import glob
        import tempfile

        before = set(glob.glob(f"{tempfile.gettempdir()}/inline_*.py"))
        inline_script_runner('print("cleanup test")')
        after = set(glob.glob(f"{tempfile.gettempdir()}/inline_*.py"))
        assert after == before, "Temp file was not cleaned up"
