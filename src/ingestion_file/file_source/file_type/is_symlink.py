from pathlib import Path

from src.ingestion_file import ValidationResult


def check_is_symlink(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa status symlink dan keberadaan target dari path
        is_symlink = path.is_symlink()
        exists = path.exists()

        # Menentukan pesan deskriptif berdasarkan kondisi symlink
        if is_symlink:
            if exists:
                # Path merupakan symlink yang mengarah ke target valid
                message = f"Path '{path}' is a valid symbolic link."
            else:
                # Path merupakan symlink tetapi mengarah ke target yang tidak ada
                message = f"Path '{path}' is a broken symbolic link (target does not exist)."
        elif not exists:
            # Path tidak ditemukan di filesystem dan bukan symlink
            message = f"Path '{path}' does not exist and is not a symbolic link."
        else:
            # Path ada di filesystem tetapi bukan symbolic link (misal: regular file/directory)
            message = f"Path '{path}' exists but is not a symbolic link."

        # Mengembalikan hasil pemeriksaan symlink (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "is_symlink",
            status = "INFO",
            actual = is_symlink,
            expected = False,
            message = message,
            details = {
                "path": str(path),
                "is_symlink": is_symlink,
                "is_broken_symlink": is_symlink and not exists
            }
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat mengakses metadata path
        return ValidationResult(
            name = "is_symlink",
            status = "ERROR",
            actual = False,
            expected = False,
            message = f"Failed to check if path '{path}' is a symlink: {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "is_symlink",
            status = "ERROR",
            actual = False,
            expected = False,
            message = f"An unexpected error occurred while checking '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )