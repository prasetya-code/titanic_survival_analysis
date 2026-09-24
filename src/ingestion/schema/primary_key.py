import csv
from collections import defaultdict


def _is_null(value):
    if value is None:
        return True

    value = str(value).strip().casefold()

    return value in {
        "",
        "null",
        "none",
        "nan",
    }


def validate_primary_key(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI PRIMARY KEY")
    print("=" * 70)

    print(f"[DEBUG] Dataset              : {dataset_name}")
    print(f"[DEBUG] File                 : {file_path}")
    print(f"[DEBUG] Schema columns      : {len(schema)}")

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            fieldnames = reader.fieldnames or []
            rows = list(reader)

    except Exception as error:
        print(f"[ERROR] Gagal membaca CSV: {error}")

        return {
            "status": "ERROR",
            "message": f"Gagal membaca CSV: {error}",
            "details": [],
        }

    csv_columns = {
        column.strip().casefold(): column
        for column in fieldnames
    }

    primary_key_columns = [
        column_name
        for column_name, column_schema in schema.items()
        if column_schema.get("semantic_type")
        == "primary_key"
    ]

    print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
    print(f"[DEBUG] Data rows            : {len(rows)}")
    print(
        f"[DEBUG] Primary key columns : "
        f"{primary_key_columns}"
    )

    if not primary_key_columns:
        print("[DEBUG] Primary key tidak didefinisikan.")
        print("[RESULT] Status            : PASS")

        return {
            "status": "PASS",
            "message": "Primary key tidak didefinisikan.",
            "details": [],
        }

    details = []
    failed = False

    actual_columns = []

    for column_name in primary_key_columns:
        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        print("-" * 70)
        print(f"[DEBUG] PK column           : {column_name}")

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print("[RESULT] Status            : FAIL")

            failed = True

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": "Primary key column tidak ditemukan.",
            })

        else:
            print(
                f"[DEBUG] Actual column       : "
                f"{actual_column}"
            )

            actual_columns.append(
                (
                    column_name,
                    actual_column,
                )
            )

    if failed:
        print("=" * 70)
        print("[RESULT] PRIMARY KEY VALIDATION")
        print("=" * 70)
        print(f"[RESULT] Dataset             : {dataset_name}")
        print("[RESULT] Status              : FAIL")

        return {
            "status": "FAIL",
            "message": (
                "Primary key column tidak lengkap "
                "di CSV."
            ),
            "details": details,
        }

    null_rows = []

    for row_number, row in enumerate(rows, start=2):
        for _, actual_column in actual_columns:
            if _is_null(row.get(actual_column)):
                null_rows.append(row_number)
                break

    print("-" * 70)
    print(
        f"[DEBUG] PK type             : "
        f"{'COMPOSITE' if len(actual_columns) > 1 else 'SINGLE'}"
    )
    print(
        f"[DEBUG] Null PK rows        : "
        f"{len(null_rows)}"
    )

    if null_rows:
        failed = True

        print(
            f"[DEBUG] Sample null rows    : "
            f"{null_rows[:10]}"
        )
        print("[RESULT] Null check         : FAIL")

        details.append({
            "status": "FAIL",
            "message": (
                f"Ditemukan {len(null_rows)} "
                "row dengan primary key null."
            ),
            "null_rows": null_rows[:50],
        })

    else:
        print("[RESULT] Null check         : PASS")

        details.append({
            "status": "PASS",
            "message": "Tidak ada primary key null.",
        })

    key_rows = defaultdict(list)

    for row_number, row in enumerate(rows, start=2):
        values = []

        for _, actual_column in actual_columns:
            value = row.get(actual_column)

            if _is_null(value):
                values.append(None)
            else:
                values.append(str(value).strip())

        key = (
            values[0]
            if len(values) == 1
            else tuple(values)
        )

        key_rows[key].append(row_number)

    duplicates = {
        key: row_numbers
        for key, row_numbers in key_rows.items()
        if len(row_numbers) > 1
        and not any(
            value is None
            for value in (
                key
                if isinstance(key, tuple)
                else [key]
            )
        )
    }

    print(
        f"[DEBUG] Duplicate PK keys  : "
        f"{len(duplicates)}"
    )

    if duplicates:
        failed = True

        print(
            f"[DEBUG] Sample duplicates   : "
            f"{dict(list(duplicates.items())[:5])}"
        )
        print("[RESULT] Unique check       : FAIL")

        details.append({
            "status": "FAIL",
            "message": (
                f"Ditemukan {len(duplicates)} "
                "duplicate primary key."
            ),
            "duplicates": dict(
                list(duplicates.items())[:20]
            ),
        })

    else:
        print("[RESULT] Unique check       : PASS")

        details.append({
            "status": "PASS",
            "message": "Primary key bersifat unique.",
        })

    status = "FAIL" if failed else "PASS"

    print("=" * 70)
    print("[RESULT] PRIMARY KEY VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Primary key         : {primary_key_columns}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Primary key validation berhasil."
            if status == "PASS"
            else "Primary key validation gagal."
        ),
        "details": details,
    }