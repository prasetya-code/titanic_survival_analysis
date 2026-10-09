from pathlib import Path

from src.ingestion_file import ValidationResult


def get_file_path(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Mengambil lokasi absolut dari path
        absolute_path = path.absolute()

        # Mengembalikan informasi jalur file absolut (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "file_path",
            status = "INFO",
            actual = str(absolute_path),
            expected = None,
            message = f"File absolute path for '{path}' retrieved: '{absolute_path}'.",
            details = {
                "path": str(path),
                "absolute_path": str(absolute_path)
            }
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O saat menyelesaikan path absolut
        return ValidationResult(
            name = "file_path",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to get file path for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "file_path",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"An unexpected error occurred while getting path for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )