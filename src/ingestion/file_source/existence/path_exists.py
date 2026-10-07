from pathlib import Path

from ..result_source import ValidationResult


def check_path_exists(path: Path) -> ValidationResult:
    path = Path(path)

    # 
    exists = path.exists()
    is_symlink = path.is_symlink()

    path_exists = exists or is_symlink

    return ValidationResult(
        name = "path_exists",
        status = "PASS" if path_exists else "FAIL",
        actual = path_exists,
        expected = True,
        message = ("Path exists." if path_exists else "Path does not exist."),
        details = {
            "path": str(path), 
            "is_symlink": is_symlink
        }
    )