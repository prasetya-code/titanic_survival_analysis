from pathlib import Path

from ..result_source import ValidationResult


def check_is_symlink(path: Path) -> ValidationResult:
    path = Path(path)

    is_symlink = path.is_symlink()

    return ValidationResult(
        name = "is_symlink",
        status = "INFO",
        actual = is_symlink,
        expected = False,
        message = ("Path is a symbolic link (shortcut or another reference file)." if is_symlink 
                   else "Path is not a symbolic link (shortcut or another reference file)."),
        details = {
            "path": str(path)
        }
    )