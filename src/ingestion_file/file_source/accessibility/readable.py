from pathlib import Path

from src.ingestion_file import ValidationResult


def check_readable(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, validasi keterbacaan dilewati (SKIP)
            return ValidationResult(
                name = "readable",
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
                name = "readable",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                },
            )

        # Mencoba membuka file dalam mode biner untuk memastikan izin baca (read access)
        with path.open("rb"):
            pass

        # Mengembalikan hasil PASS jika file berhasil dibuka
        return ValidationResult(
            name = "readable",
            status = "PASS",
            actual = True,
            expected = True,
            message = f"File '{path}' is readable.",
            details = {
                "path": str(path)
            },
        )

    except (OSError, PermissionError) as error:
        # Menangani kegagalan akses baca (misal: permission denied) atau error OS
        return ValidationResult(
            name = "readable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File '{path}' is not readable: {error}",
            details = {
                "path": str(path), 
                "error": str(error)
            },
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "readable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"An unexpected error occurred while reading '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            },
        )