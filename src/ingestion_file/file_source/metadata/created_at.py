from datetime import datetime
from pathlib import Path

from src.ingestion_file import ValidationResult


def get_created_at(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path atau status symlink
        if not path.exists() and not path.is_symlink():
            # Jika path tidak ada dan bukan symlink, validasi dilewati (SKIP)
            return ValidationResult(
                name = "created_at",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil metadata statistik file
        stat_result = path.stat()

        # Mencoba menggunakan st_birthtime (tersedia di macOS/Windows), jika tidak ada fallback ke st_ctime
        try:
            timestamp = stat_result.st_birthtime
        except AttributeError:
            # Pada Linux/POSIX, st_birthtime tidak selalu tersedia sehingga digunakan st_ctime (change time)
            timestamp = stat_result.st_ctime

        # Mengonversi timestamp ke format string ISO
        value = datetime.fromtimestamp(timestamp).isoformat()

        # Mengembalikan informasi waktu pembuatan file (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "created_at",
            status = "INFO",
            actual = value,
            expected = None,
            message = f"File '{path}' created at: {value}.",
            details = {
                "path": str(path),
                "timestamp": timestamp,
                "datetime": value
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat membaca metadata statistik file
        return ValidationResult(
            name = "created_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read creation time for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "created_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"An unexpected error occurred while reading creation time for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )