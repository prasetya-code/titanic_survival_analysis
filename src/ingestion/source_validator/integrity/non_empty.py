from pathlib import Path

from ..result_source import ValidationResult


def check_non_empty(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists():
        return ValidationResult(
            name = "non_empty",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "File does not exist."
        )

    if not path.is_file():
        return ValidationResult(
            name = "non_empty",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "Path is not a regular file."
        )

    try:
        size = path.stat().st_size
        non_empty = size > 0

        return ValidationResult(
            name = "non_empty",
            status = "PASS" if non_empty else "FAIL",
            actual = non_empty,
            expected = True,
            message = ("File is not empty." if non_empty else "File is empty."),
            details = {
                "size_bytes": size
            },
        )

    except OSError as error:
        return ValidationResult(
            name = "non_empty",
            status = "ERROR",
            actual = None,
            expected = True,
            message = f"Failed to check file size: {error}"
        )