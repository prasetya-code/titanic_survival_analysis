from pathlib import Path

from ..result_source import ValidationResult


def check_file_exists(path: Path) -> ValidationResult:
    path = Path(path)

    # 
    exists = path.exists()
    is_file = path.is_file()

    result = exists and is_file

    if result:
        message = "File exists."

    elif not exists:
        message = "File does not exist."

    else:
        message = "Path exists but is not a file."

    return ValidationResult(
        name = "file_exists",
        status = "PASS" if result else "FAIL",
        actual = result,
        expected = True,
        message = message,
        details = {
            "path": str(path), 
            "exists": exists, 
            "is_file": is_file
        }
    )