import csv
from pathlib import Path


def detect_delimiter(file_path: Path) -> str:
    """
    Mendeteksi delimiter file text.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            sample = file.read(4096)

            if not sample.strip():
                return ","

            dialect = csv.Sniffer().sniff(
                sample,
                delimiters=",;\t|"
            )

            return dialect.delimiter

    except Exception:
        return ","


def read_text_metadata(file_path: Path) -> dict:
    """
    Membaca metadata CSV / TSV / TXT.
    """

    delimiter = detect_delimiter(file_path)

    row_count = 0
    empty_rows = 0
    inconsistent_rows = 0
    columns = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.reader(
            file,
            delimiter=delimiter
        )

        try:
            header = next(reader)

        except StopIteration:
            return {
                "encoding": "UTF-8",
                "delimiter": delimiter,
                "has_header": False,
                "columns": [],
                "column_count": 0,
                "row_count": 0,
                "empty_rows": 0,
                "inconsistent_rows": 0,
            }

        columns = [
            column.strip()
            for column in header
        ]

        expected_column_count = len(columns)

        for row in reader:

            if not row or all(
                str(value).strip() == ""
                for value in row
            ):
                empty_rows += 1
                continue

            row_count += 1

            if len(row) != expected_column_count:
                inconsistent_rows += 1

    return {
        "encoding": "UTF-8",
        "delimiter": delimiter,
        "has_header": True,
        "columns": columns,
        "column_count": len(columns),
        "row_count": row_count,
        "empty_rows": empty_rows,
        "inconsistent_rows": inconsistent_rows,
    }