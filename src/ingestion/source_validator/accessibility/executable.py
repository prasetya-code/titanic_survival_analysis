import os
from pathlib import Path

from ..result_source import ValidationResult


def check_executable(path: Path) -> ValidationResult:
    path = Path(path)

    # 
    if not path.exists():
        return ValidationResult(
            name = "executable",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "File does not exist.",
            details = {
                "path": str(path)
            },
        )

    # 
    if not path.is_file():
        return ValidationResult(
            name = "executable",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "Path is not a regular file.",
            details = {
                "path": str(path)
            },
        )

    executable  =  os.access(path, os.X_OK)

    return ValidationResult(
        name = "executable",
        status = "INFO",
        actual = executable,
        expected = False,
        message = ("File is executable." if executable else "File is not executable."),
        details = {
            "path": str(path)
        },
    )