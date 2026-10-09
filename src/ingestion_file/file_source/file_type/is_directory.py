from pathlib import Path

from src.ingestion_file import ValidationResult


def check_is_directory(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path, tipe direktori, dan status symlink
        exists = path.exists()
        is_symlink = path.is_symlink()
        is_directory = path.is_dir()

        # Menentukan pesan deskriptif berdasarkan status kondisi path
        if is_directory:
            if is_symlink:
                # Path merupakan direktori yang diakses via symlink
                message = f"Path '{path}' is a directory (symlink target)."
            else:
                # Path merupakan direktori biasa
                message = f"Path '{path}' is a directory."
        elif not exists:
            if is_symlink:
                # Path adalah broken symlink sehingga tidak terdeteksi sebagai direktori
                message = f"Path '{path}' is not a directory (broken symlink)."
            else:
                # Path tidak ditemukan di filesystem
                message = f"Path '{path}' does not exist."
        else:
            # Path ada di filesystem tetapi bukan direktori (misalnya regular file)
            message = f"Path '{path}' exists but is not a directory (e.g. regular file)."

        # Mengembalikan hasil pemeriksaan direktori (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "is_directory",
            status = "INFO",
            actual = is_directory,
            expected = False,
            message = message,
            details = {
                "path": str(path),
                "exists": exists,
                "is_directory": is_directory,
                "is_symlink": is_symlink
            }
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat memeriksa atribut path
        return ValidationResult(
            name = "is_directory",
            status = "ERROR",
            actual = False,
            expected = False,
            message = f"Failed to check if path '{path}' is a directory: {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "is_directory",
            status = "ERROR",
            actual = False,
            expected = False,
            message = f"An unexpected error occurred while checking '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )