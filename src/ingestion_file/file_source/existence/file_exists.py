from pathlib import Path

from src.ingestion_file import ValidationResult


def check_file_exists(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path, status file, dan tipe symlink
        exists = path.exists()
        is_symlink = path.is_symlink()
        is_file = path.is_file()

        # Validasi berhasil jika path ada DAN dipastikan berupa file
        result = exists and is_file

        # Menentukan pesan deskriptif berdasarkan kondisi path
        if result:
            if is_symlink:
                # File ada dan diakses melalui symlink yang valid
                message = f"File '{path}' exists and is a valid symlink."
            else:
                # File biasa ada
                message = f"File '{path}' exists."
        elif not exists:
            if is_symlink:
                # Kasus khusus: Symlink ada tetapi merujuk ke target file yang hilang
                message = f"File '{path}' exists as a broken symlink."
            else:
                # File tidak ditemukan di filesystem
                message = f"File '{path}' does not exist."
        else:
            # Path ada di filesystem tetapi bukan file (misalnya direktori)
            message = f"Path '{path}' exists but is not a file."

        # Mengembalikan hasil validasi sukses
        return ValidationResult(
            name = "file_exists",
            status = "PASS" if result else "FAIL",
            actual = result,
            expected = True,
            message = message,
            details = {
                "path": str(path), 
                "exists": exists, 
                "is_file": is_file,
                "is_symlink": is_symlink,
                "is_broken_symlink": is_symlink and not exists
            }
        )
    except Exception as e:
        # Menangani exception yang mungkin terjadi (misal: PermissionError, OSError)
        return ValidationResult(
            name = "file_exists",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"Failed to check file '{path}': {str(e)}",
            details = {
                "path": str(path),
                "error": str(e)
            }
        )