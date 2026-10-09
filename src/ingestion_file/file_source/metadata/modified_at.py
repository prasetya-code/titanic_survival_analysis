from datetime import datetime
from pathlib import Path

from src.ingestion_file import ValidationResult


def get_modified_at(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path atau status symlink
        if not path.exists() and not path.is_symlink():
            # Jika path tidak ada dan bukan symlink, validasi dilewati (SKIP)
            return ValidationResult(
                name = "modified_at",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil timestamp waktu modifikasi terakhir (st_mtime)
        timestamp = path.stat().st_mtime
        value = datetime.fromtimestamp(timestamp).isoformat()

        # Mengembalikan informasi waktu modifikasi file (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "modified_at",
            status = "INFO",
            actual = value,
            expected = None,
            message = f"File '{path}' modified at: {value}.",
            details = {
                "path": str(path),
                "timestamp": timestamp,
                "datetime": value
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat membaca metadata statistik file
        return ValidationResult(
            name = "modified_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read modification time for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "modified_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"An unexpected error occurred while reading modification time for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )