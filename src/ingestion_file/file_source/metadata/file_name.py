from pathlib import Path

from src.ingestion_file import ValidationResult


def get_file_name(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Mengambil nama file/komponen terakhir dari path
        file_name = path.name

        # Menentukan pesan deskriptif berdasarkan ketersediaan nama file
        if file_name:
            message = f"File name for '{path}' retrieved: '{file_name}'."
        else:
            # Kasus khusus jika path menunjuk ke root (misalnya '/' atau '.')
            message = f"Path '{path}' does not contain a specific file name (root path)."

        # Mengembalikan hasil ekstraksi nama file (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "file_name",
            status = "INFO",
            actual = file_name or None,
            expected = None,
            message = message,
            details = {
                "path": str(path),
                "file_name": file_name
            }
        )

    except Exception as error:
        # Menangani exception tak terduga saat membaca properti path
        return ValidationResult(
            name = "file_name",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to retrieve file name for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )