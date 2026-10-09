from datetime import datetime
from pathlib import Path
import json

from src.config import FINGERPRINT_FILE


def load_file_fingerprint(
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> dict:
    """Memuat data fingerprint dari file JSON metadata."""
    fingerprint_file = Path(fingerprint_file)

    if not fingerprint_file.exists():
        return {}

    try:
        with fingerprint_file.open("r", encoding = "utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return {}


def save_file_fingerprint(
    file_path: Path,
    file_hash: str,
    file_key: str,
    fingerprint_file: Path = FINGERPRINT_FILE,
    version: int = 1,
) -> dict:
    """Menyimpan atau memperbarui record fingerprint file beserta riwayat versioning."""
    file_path = Path(file_path)
    fingerprint_file = Path(fingerprint_file)

    try:
        fingerprint_file.parent.mkdir(
            parents = True,
            exist_ok = True,
        )

        fingerprints = load_file_fingerprint(fingerprint_file)
        existing_record = fingerprints.get(file_key, {})
        history = existing_record.get("history", [])

        # Jika memperbarui versi, masukkan versi lama ke dalam history
        if "file_hash" in existing_record and existing_record["file_hash"] != file_hash:
            history.append({
                "version": existing_record.get("version", 1),
                "file_hash": existing_record.get("file_hash"),
                "updated_at": existing_record.get("updated_at"),
            })

        current_time = datetime.now().isoformat()

        updated_record = {
            "file_name": file_path.name,
            "file_path": str(file_path.resolve()),
            "file_hash": file_hash,
            "version": version,
            "updated_at": current_time,
            "history": history,
        }

        fingerprints[file_key] = updated_record

        with fingerprint_file.open("w", encoding = "utf-8") as file:
            json.dump(
                fingerprints,
                file,
                indent = 4,
                ensure_ascii = False,
            )

        return updated_record

    except Exception:
        return {}