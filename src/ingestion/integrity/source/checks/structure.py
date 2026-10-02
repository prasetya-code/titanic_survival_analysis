# source_validator/checks/structure.py

from pathlib import Path

from ..metadata.reader import read_file_metadata


def check_structure(
    file_path: Path,
) -> dict:
    """
    Memvalidasi struktur file.
    """

    metadata = read_file_metadata(
        file_path
    )

    if not metadata["has_header"]:

        return {
            "status": "FAIL",
            "actual": metadata,
            "expected": {
                "has_header": True,
            },
            "message": (
                "Data file tidak memiliki header."
            ),
        }

    if metadata["column_count"] == 0:

        return {
            "status": "FAIL",
            "actual": metadata,
            "expected": {
                "column_count": "> 0",
            },
            "message": (
                "Data file tidak memiliki kolom."
            ),
        }

    if metadata["inconsistent_rows"] > 0:

        return {
            "status": "FAIL",
            "actual": metadata,
            "expected": {
                "inconsistent_rows": 0,
            },
            "message": (
                f"Data file memiliki "
                f"{metadata['inconsistent_rows']} "
                f"baris dengan jumlah kolom "
                f"tidak konsisten."
            ),
        }

    return {
        "status": "PASS",
        "actual": metadata,
        "expected": {
            "has_header": True,
            "column_count": "> 0",
            "inconsistent_rows": 0,
        },
        "message": "Struktur data valid.",
    }