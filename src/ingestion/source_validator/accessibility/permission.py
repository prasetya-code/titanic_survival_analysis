import stat
from pathlib import Path

from ..result_source import ValidationResult


def check_permission(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists():
        return ValidationResult(
            name = "permission",
            status = "SKIP",
            actual = None,
            expected = None,
            message = "Path does not exist.",
            details = {
                "path": str(path),
            },
        )

    try:
        mode  =  path.stat().st_mode

        return ValidationResult(
            name = "permission",
            status = "INFO",
            actual = {
                "mode": stat.filemode(mode),
                "octal": oct(stat.S_IMODE(mode)),
            },
            expected = None,
            message = "File permission retrieved.",
            details = {
                "path": str(path),
                "mode": stat.filemode(mode),
                "octal": oct(stat.S_IMODE(mode)),
            },
        )

    except OSError as error:
        return ValidationResult(
            name = "permission",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read permission: {error}",
            details = {
                "path": str(path),
                "error": str(error),
            },
        )