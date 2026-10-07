from pathlib import Path

from ..result_source import ValidationResult


def check_target_exists(path: Path) -> ValidationResult:
    path = Path(path)

    # 
    if not path.is_symlink():
        return ValidationResult(
            name = "target_exists",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "Path is not a symbolic link (shortcut or another reference file).",
            details = {
                "path": str(path)
            },
        )

    try:
        target = path.resolve(strict = False)
        target_exists = target.exists()

        return ValidationResult(
            name = "target_exists",
            status = "PASS" if target_exists else "FAIL",
            actual = target_exists,
            expected = True,
            message = ("Symbolic link target exists." if target_exists else "Symbolic link target does not exist."),
            details={
                "path": str(path), 
                "target": str(target)
            },
        )

    except OSError as error:
        return ValidationResult(
            name = "target_exists",
            status = "ERROR",
            actual = None,
            expected = True,
            message = f"Failed to resolve symbolic link: {error}",
            details = {
                "path": str(path)
            },
        )