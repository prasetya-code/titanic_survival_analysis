from pathlib import Path

from src.ingestion_file import ValidationResult


def check_non_empty(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, pengecekan kekosongan dilewati (SKIP)
            return ValidationResult(
                name = "non_empty",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                }
            )

        # Memeriksa apakah path merupakan file biasa (regular file)
        if not path.is_file():
            # Jika path berupa direktori atau objek lain, pengecekan dilewati (SKIP)
            return ValidationResult(
                name = "non_empty",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil ukuran file dalam bytes
        size = path.stat().st_size
        non_empty = size > 0

        # Menentukan pesan deskriptif berdasarkan status kekosongan file
        if non_empty:
            message = f"File '{path}' is not empty ({size:,} bytes)."
        else:
            message = f"File '{path}' is empty (0 bytes)."

        # Mengembalikan hasil validasi keterisian file
        return ValidationResult(
            name = "non_empty",
            status = "PASS" if non_empty else "FAIL",
            actual = non_empty,
            expected = True,
            message = message,
            details = {
                "path": str(path),
                "size_bytes": size,
                "non_empty": non_empty
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat membaca statistik file
        return ValidationResult(
            name = "non_empty",
            status = "ERROR",
            actual = None,
            expected = True,
            message = f"Failed to check file size for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "non_empty",
            status = "ERROR",
            actual = None,
            expected = True,
            message = f"An unexpected error occurred while checking file size for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )