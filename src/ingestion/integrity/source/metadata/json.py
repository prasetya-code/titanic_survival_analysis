import json
from pathlib import Path


def _empty_metadata():
    return {
        "encoding": "UTF-8",
        "delimiter": None,
        "has_header": False,
        "columns": [],
        "column_count": 0,
        "row_count": 0,
        "empty_rows": 0,
        "inconsistent_rows": 0,
    }


def _extract_object_columns(records):
    """
    Mengambil union seluruh key dari object.
    """

    columns = []

    for record in records:
        columns.extend(record.keys())

    return list(dict.fromkeys(columns))


def _read_jsonl(file_path: Path) -> dict:
    """
    Membaca JSONL.
    """

    records = []
    empty_rows = 0

    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        for line in file:

            if not line.strip():
                empty_rows += 1
                continue

            record = json.loads(line)
            records.append(record)

    if not records:
        metadata = _empty_metadata()
        metadata["empty_rows"] = empty_rows
        return metadata

    if all(
        isinstance(record, dict)
        for record in records
    ):

        columns = _extract_object_columns(
            records
        )

        return {
            "encoding": "UTF-8",
            "delimiter": None,
            "has_header": True,
            "columns": columns,
            "column_count": len(columns),
            "row_count": len(records),
            "empty_rows": empty_rows,
            "inconsistent_rows": 0,
        }

    return {
        "encoding": "UTF-8",
        "delimiter": None,
        "has_header": False,
        "columns": [],
        "column_count": 0,
        "row_count": len(records),
        "empty_rows": empty_rows,
        "inconsistent_rows": 0,
    }


def read_json_metadata(file_path: Path) -> dict:
    """
    Membaca JSON atau JSONL.
    """

    if file_path.suffix.lower() == ".jsonl":
        return _read_jsonl(file_path)

    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        content = file.read().strip()

    if not content:
        return _empty_metadata()

    data = json.loads(content)

    # JSON array
    if isinstance(data, list):

        row_count = len(data)

        if not data:
            return {
                "encoding": "UTF-8",
                "delimiter": None,
                "has_header": False,
                "columns": [],
                "column_count": 0,
                "row_count": 0,
                "empty_rows": 0,
                "inconsistent_rows": 0,
            }

        # Array of objects
        if all(
            isinstance(record, dict)
            for record in data
        ):

            columns = _extract_object_columns(data)

            return {
                "encoding": "UTF-8",
                "delimiter": None,
                "has_header": True,
                "columns": columns,
                "column_count": len(columns),
                "row_count": row_count,
                "empty_rows": 0,
                "inconsistent_rows": 0,
            }

        # Array of arrays
        if all(
            isinstance(record, list)
            for record in data
        ):

            max_columns = max(
                len(record)
                for record in data
            )

            columns = [
                f"column_{index}"
                for index in range(
                    1,
                    max_columns + 1
                )
            ]

            inconsistent_rows = sum(
                len(record) != max_columns
                for record in data
            )

            return {
                "encoding": "UTF-8",
                "delimiter": None,
                "has_header": False,
                "columns": columns,
                "column_count": len(columns),
                "row_count": row_count,
                "empty_rows": 0,
                "inconsistent_rows": inconsistent_rows,
            }

    # JSON object
    if isinstance(data, dict):

        columns = list(data.keys())

        return {
            "encoding": "UTF-8",
            "delimiter": None,
            "has_header": True,
            "columns": columns,
            "column_count": len(columns),
            "row_count": 1,
            "empty_rows": 0,
            "inconsistent_rows": 0,
        }

    # JSON scalar
    return {
        "encoding": "UTF-8",
        "delimiter": None,
        "has_header": False,
        "columns": [],
        "column_count": 0,
        "row_count": 1,
        "empty_rows": 0,
        "inconsistent_rows": 0,
    }