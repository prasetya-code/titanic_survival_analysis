from pathlib import Path

from ..result_source import ValidationResult


def check_openable(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists():
        return ValidationResult(
            name = "openable",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "File does not exist."
        )

    if not path.is_file():
        return ValidationResult(
            name = "openable",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "Path is not a regular file."
        )

    try:
        with path.open("rb"):
            pass

        return ValidationResult(
            name = "openable",
            status = "PASS",
            actual = True,
            expected = True,
            message = "File can be opened successfully."
        )

    except (OSError, PermissionError) as error:
        return ValidationResult(
            name = "openable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File cannot be opened: {error}",
            details = {
                "error": str(error)
            },
        )