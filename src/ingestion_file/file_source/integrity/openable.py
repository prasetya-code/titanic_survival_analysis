from pathlib import Path

from src.ingestion_file import ValidationResult


def check_openable(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, pengujian pembukaan file dilewati (SKIP)
            return ValidationResult(
                name = "openable",
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
            # Jika path berupa direktori atau objek lain, pengujian dilewati (SKIP)
            return ValidationResult(
                name = "openable",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                }
            )

        # Mencoba membuka file dalam mode biner untuk memverifikasi keterbukaan (openability)
        with path.open("rb"):
            pass

        # Mengembalikan hasil jika file berhasil dibuka
        return ValidationResult(
            name = "openable",
            status = "PASS",
            actual = True,
            expected = True,
            message = f"File '{path}' can be opened successfully.",
            details = {
                "path": str(path),
                "openable": True
            }
        )

    except (OSError, PermissionError) as error:
        # Menangani kesalahan akses, I/O, atau izin saat membuka file
        return ValidationResult(
            name = "openable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File '{path}' cannot be opened: {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )

    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "openable",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"An unexpected error occurred while opening file '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )