# source_validator/metadata/parquet.py

from pathlib import Path

import pyarrow.parquet as pq


def read_parquet_metadata(file_path: Path) -> dict:
    """
    Membaca metadata Parquet.
    """

    parquet_file = pq.ParquetFile(
        file_path
    )

    schema = parquet_file.schema_arrow

    columns = list(schema.names)

    return {
        "encoding": "Parquet",
        "delimiter": None,
        "has_header": True,
        "columns": columns,
        "column_count": len(columns),
        "row_count": parquet_file.metadata.num_rows,
        "empty_rows": 0,
        "inconsistent_rows": 0,
    }