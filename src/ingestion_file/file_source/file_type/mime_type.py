import mimetypes
from pathlib import Path

from src.ingestion_file import ValidationResult


def check_mime_type(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        exists = path.exists()

        # Mendeteksi MIME type dan encoding berdasarkan nama file
        mime_type, encoding = mimetypes.guess_type(path.name)

        # Menentukan pesan deskriptif berdasarkan ketersediaan MIME type dan status path
        if mime_type:
            if encoding:
                message = f"MIME type for '{path}' detected: {mime_type} (encoding: {encoding})."
            else:
                message = f"MIME type for '{path}' detected: {mime_type}."
        elif not exists:
            message = f"MIME type for '{path}' could not be detected (path does not exist)."
        else:
            message = f"MIME type for '{path}' could not be detected."

        # Mengembalikan hasil deteksi MIME type (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "mime_type",
            status = "INFO",
            actual = mime_type,
            expected = None,
            message = message,
            details = {
                "path": str(path),
                "mime_type": mime_type,
                "encoding": encoding,
                "exists": exists
            }
        )

    except Exception as error:
        # Menangani exception tak terduga
        return ValidationResult(
            name = "mime_type",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to detect MIME type for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            }
        )