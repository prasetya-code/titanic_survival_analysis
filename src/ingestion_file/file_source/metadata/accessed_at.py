from datetime import datetime
from pathlib import Path

from src.ingestion_file import ValidationResult


def get_accessed_at(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path atau status symlink
        if not path.exists() and not path.is_symlink():
            # Jika path tidak ada dan bukan symlink, validasi dilewati (SKIP)
            return ValidationResult(
                name = "accessed_at",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil timestamp waktu akses terakhir (st_atime)
        timestamp = path.stat().st_atime
        value = datetime.fromtimestamp(timestamp).isoformat()

        # Mengembalikan informasi waktu akses file (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "accessed_at",
            status = "INFO",
            actual = value,
            expected = None,
            message = f"File '{path}' accessed at: {value}.",
            details = {
                "path": str(path),
                "timestamp": timestamp,
                "datetime": value
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat membaca metadata statistik file
        return ValidationResult(
            name = "accessed_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read access time for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "accessed_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"An unexpected error occurred while reading access time for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )