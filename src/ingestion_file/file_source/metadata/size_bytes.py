from pathlib import Path

from src.ingestion_file import ValidationResult


def _format_size(size_bytes: int) -> str:
    """Mengonversi ukuran bytes menjadi format teks yang mudah dibaca manusia."""
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size_bytes:.2f} B"


def get_size_bytes(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path atau status symlink
        if not path.exists() and not path.is_symlink():
            # Jika path tidak ada dan bukan symlink, validasi dilewati (SKIP)
            return ValidationResult(
                name = "size_bytes",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil ukuran file/path dalam hitungan bytes
        size = path.stat().st_size
        human_size = _format_size(size)

        # Mengembalikan informasi ukuran file (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "size_bytes",
            status = "INFO",
            actual = size,
            expected = None,
            message = f"File size for '{path}': {human_size} ({size:,} bytes).",
            details = {
                "path": str(path),
                "size_bytes": size,
                "size_human": human_size
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat membaca metadata statistik file
        return ValidationResult(
            name = "size_bytes",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read file size for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "size_bytes",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"An unexpected error occurred while checking file size for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )