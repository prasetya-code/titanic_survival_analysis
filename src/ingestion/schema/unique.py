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


def validate_unique(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI UNIQUE")
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

    print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
    print(f"[DEBUG] Data rows            : {len(rows)}")

    details = []
    failed_columns = []
    validated_columns = 0

    for column_name, column_schema in schema.items():
        is_unique = column_schema.get("unique")

        if is_unique is not True:
            continue

        validated_columns += 1

        print("-" * 70)
        print(f"[DEBUG] Column              : {column_name}")
        print("[DEBUG] Unique              : True")

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print("[RESULT] Status            : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": "Kolom tidak ditemukan di CSV.",
            })

            continue

        value_rows = defaultdict(list)

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if _is_null(value):
                continue

            normalized_value = str(value).strip()

            value_rows[normalized_value].append(
                row_number
            )

        duplicates = {
            value: row_numbers
            for value, row_numbers in value_rows.items()
            if len(row_numbers) > 1
        }

        duplicate_count = len(duplicates)

        print(
            f"[DEBUG] Duplicate values    : "
            f"{duplicate_count}"
        )

        if duplicates:
            print(
                f"[DEBUG] Sample duplicates   : "
                f"{dict(list(duplicates.items())[:5])}"
            )
            print("[RESULT] Status            : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    f"Ditemukan {duplicate_count} "
                    "nilai duplicate."
                ),
                "duplicates": dict(
                    list(duplicates.items())[:20]
                ),
            })

        else:
            print("[RESULT] Status            : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": "Semua nilai unique.",
            })

    if validated_columns == 0:
        print(
            "[DEBUG] Tidak ada kolom dengan "
            "unique=True dalam schema."
        )

    status = "FAIL" if failed_columns else "PASS"

    print("=" * 70)
    print("[RESULT] UNIQUE VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Unique validation berhasil."
            if status == "PASS"
            else "Terdapat nilai duplicate."
        ),
        "details": details,
    }