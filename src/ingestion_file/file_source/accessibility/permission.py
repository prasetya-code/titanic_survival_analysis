import stat
from pathlib import Path

from src.ingestion_file import ValidationResult


def check_permission(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika path tidak ada, pengecekan izin dilewati (SKIP)
            return ValidationResult(
                name = "permission",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path),
                },
            )

        # Mengambil informasi metadata status file
        mode = path.stat().st_mode
        file_mode_str = stat.filemode(mode)
        octal_str = oct(stat.S_IMODE(mode))

        # Mengembalikan informasi izin akses file (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "permission",
            status = "INFO",
            actual = {
                "mode": file_mode_str,
                "octal": octal_str,
            },
            expected = None,
            message = f"File permission for '{path}' retrieved: {file_mode_str} ({octal_str}).",
            details = {
                "path": str(path),
                "mode": file_mode_str,
                "octal": octal_str,
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat membaca metadata statistik file
        return ValidationResult(
            name = "permission",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read permission for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error),
            },
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "permission",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"An unexpected error occurred while reading permission for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error),
            },
        )