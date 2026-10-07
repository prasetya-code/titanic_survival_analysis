from pathlib import Path

from ..result_source import ValidationResult


def check_readable(path: Path) -> ValidationResult:
    path = Path(path)

    # 
    if not path.exists():
        return ValidationResult(
            name = "readable",
            status = "SKIP",
            actual= None,
            expected = True,
            message = "File does not exist.",
            details = {
                "path": str(path)
            },
        )

    # 
    if not path.is_file():
        return ValidationResult(
            name = "readable",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "Path is not a regular file.",
            details={
                "path": str(path)
            },
        )

    try:
        with path.open("rb"):
            pass

        return ValidationResult(
            name = "readable",
            status = "PASS",
            actual = True,
            expected = True,
            message = "File is readable.",
            details = {
                "path": str(path)
            },
        )

    except (OSError, PermissionError) as error:
        return ValidationResult(
            name = "readable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File is not readable: {error}",
            details = {
                "path": str(path), 
                "error": str(error)
            },
        )