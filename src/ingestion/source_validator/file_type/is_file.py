from pathlib import Path

from ..result_source import ValidationResult


def check_is_file(path: Path) -> ValidationResult:
    path = Path(path)

    is_file = path.is_file()

    return ValidationResult(
        name = "is_file",
        status = "PASS" if is_file else "FAIL",
        actual = is_file,
        expected = True,
        message = ("Path is a regular file." if is_file else "Path is not a regular file."),
        details = {
            "path": str(path)
        }
    )