from pathlib import Path
from src.config import INGESTION_SUPP_EXT
from src.ingestion_file import ValidationResult


def check_extension(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Mengambil ekstensi file dalam huruf kecil
        extension = path.suffix.lower()

        # Memeriksa apakah ekstensi didukung berdasarkan kamus SUPPORTED_EXTENSIONS
        supported = extension in INGESTION_SUPP_EXT
        format_name = INGESTION_SUPP_EXT.get(extension)

        # Menentukan pesan deskriptif berdasarkan status dukungan ekstensi
        if supported:
            message = f"File '{path}' has a supported extension '{extension}' ({format_name})."
        elif not extension:
            message = f"File '{path}' has no file extension."
        else:
            message = f"File '{path}' has an unsupported extension '{extension}'."

        # Mengembalikan hasil validasi ekstensi
        return ValidationResult(
            name = "extension",
            status = "PASS" if supported else "FAIL",
            actual = extension or None,
            expected = list(INGESTION_SUPP_EXT.keys()),
            message = message,
            details = {
                "path": str(path),
                "extension": extension or None,
                "format": format_name,
                "supported": supported
            }
        )

    except Exception as error:
        # Menangani exception tak terduga (misal: penanganan objek path yang tidak valid)
        return ValidationResult(
            name = "extension",
            status = "FAIL",
            actual = None,
            expected = list(INGESTION_SUPP_EXT.keys()),
            message = f"Failed to check file extension for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )