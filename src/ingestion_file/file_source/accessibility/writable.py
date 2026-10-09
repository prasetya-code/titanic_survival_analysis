from pathlib import Path

from src.ingestion_file import ValidationResult


def check_writable(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, validasi keterulisan dilewati (SKIP)
            return ValidationResult(
                name = "writable",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                },
            )

        # Memeriksa apakah path merupakan file biasa (regular file)
        if not path.is_file():
            # Jika path berupa direktori atau objek lain, validasi dilewati (SKIP)
            return ValidationResult(
                name = "writable",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                },
            )

        # Mencoba membuka file dalam mode append binary ("ab") untuk menguji izin tulis tanpa merusak konten
        with path.open("ab"):
            pass

        # Mengembalikan hasil PASS jika file berhasil dibuka dalam mode tulis
        return ValidationResult(
            name = "writable",
            status = "PASS",
            actual = True,
            expected = True,
            message = f"File '{path}' is writable.",
            details = {
                "path": str(path)
            },
        )

    except (OSError, PermissionError) as error:
        # Menangani kegagalan akses tulis (misal: read-only filesystem atau permission denied)
        return ValidationResult(
            name = "writable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File '{path}' is not writable: {error}",
            details = {
                "path": str(path), 
                "error": str(error)
            },
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "writable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"An unexpected error occurred while checking writability for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            },
        )