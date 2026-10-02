# source_validator/checks/existence.py

from pathlib import Path


def check_existence(file_path: Path) -> dict:
    """
    Check apakah filesystem entry tersedia.

    Broken symlink tetap dianggap sebagai entry.
    """

    exists = file_path.exists()
    is_symlink = file_path.is_symlink()

    path_entry_exists = (
        exists or is_symlink
    )

    if not path_entry_exists:

        return {
            "status": "FAIL",
            "actual": (
                f"{file_path} does not exist"
            ),
            "expected": (
                "file/path entry exists"
            ),
            "message": (
                f"Source file tidak ditemukan: "
                f"{file_path}"
            ),
        }

    return {
        "status": "PASS",
        "actual": path_entry_exists,
        "expected": True,
        "message": "Path tersedia.",
    }