from pathlib import Path

from src.ingestion_file import ValidationResult


def check_is_file(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path dan apakah path tersebut merupakan file biasa (regular file)
        exists = path.exists()
        is_symlink = path.is_symlink()
        is_file = path.is_file()

        # Menentukan pesan deskriptif berdasarkan status kondisi path
        if is_file:
            if is_symlink:
                # Path merupakan file biasa yang diakses via symlink
                message = f"Path '{path}' is a regular file (symlink target)."
            else:
                # Path merupakan file biasa
                message = f"Path '{path}' is a regular file."
        elif not exists:
            if is_symlink:
                # Path adalah broken symlink sehingga tidak terdeteksi sebagai file
                message = f"Path '{path}' is not a file (broken symlink)."
            else:
                # Path tidak ditemukan di filesystem
                message = f"Path '{path}' does not exist."
        else:
            # Path ada tetapi bukan file (misalnya direktori)
            message = f"Path '{path}' exists but is not a regular file (e.g. directory)."

        # Mengembalikan hasil validasi status file
        return ValidationResult(
            name = "is_file",
            status = "PASS" if is_file else "FAIL",
            actual = is_file,
            expected = True,
            message = message,
            details = {
                "path": str(path),
                "exists": exists,
                "is_file": is_file,
                "is_symlink": is_symlink
            }
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat memeriksa atribut file
        return ValidationResult(
            name = "is_file",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"Failed to check if path '{path}' is a file: {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "is_file",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"An unexpected error occurred while checking '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )