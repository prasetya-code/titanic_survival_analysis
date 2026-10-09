from pathlib import Path

from src.ingestion_file import ValidationResult


def check_path_exists(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path dan apakah path tersebut merupakan symlink
        exists = path.exists()
        is_symlink = path.is_symlink()

        # Path dianggap ada jika targetnya ada ATAU merupakan symlink (meskipun broken symlink)
        path_exists = exists or is_symlink

        # Menentukan pesan deskriptif berdasarkan status keberadaan dan tipe path
        if path_exists:
            if is_symlink and not exists:
                # Kasus khusus: Symlink ada, tetapi merujuk ke target yang tidak ditemukan
                message = f"Path '{path}' exists as a broken symlink."
            elif is_symlink:
                # Symlink ada dan merujuk ke target yang valid
                message = f"Path '{path}' exists and is a valid symlink."
            else:
                # Path biasa ada
                message = f"Path '{path}' exists."
        else:
            # Path tidak ditemukan di filesystem
            message = f"Path '{path}' does not exist."

        # Mengembalikan hasil validasi sukses
        return ValidationResult(
            name = "path_exists",
            status = "PASS" if path_exists else "FAIL",
            actual = path_exists,
            expected = True,
            message = message,
            details = {
                "path": str(path),
                "is_symlink": is_symlink,
                "is_broken_symlink": is_symlink and not exists
            }
        )
    except Exception as e:
        # Menangani exception yang mungkin terjadi (misal: PermissionError, OSError)
        return ValidationResult(
            name = "path_exists",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"Failed to check path '{path}': {str(e)}",
            details = {
                "path": str(path),
                "error": str(e)
            }
        )