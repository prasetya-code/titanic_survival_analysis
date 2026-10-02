# source_validator/metadata/reader.py

from pathlib import Path

from .text import read_text_metadata
from .json import read_json_metadata
from .excel import read_excel_metadata
from .parquet import read_parquet_metadata


METADATA_READERS = {
    ".csv": read_text_metadata,
    ".tsv": read_text_metadata,
    ".txt": read_text_metadata,
    ".json": read_json_metadata,
    ".jsonl": read_json_metadata,
    ".xlsx": read_excel_metadata,
    ".parquet": read_parquet_metadata,
}


def read_file_metadata(file_path: Path) -> dict:
    """
    Dispatcher metadata berdasarkan extension.
    """

    extension = file_path.suffix.lower()

    reader = METADATA_READERS.get(
        extension
    )

    if reader is None:
        raise ValueError(
            f"Format file "
            f"'{extension or '(none)'}' "
            f"belum didukung."
        )

    return reader(file_path)