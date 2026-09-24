import csv
import re
from datetime import datetime


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


def _is_valid_format(value, expected_format):
    if _is_null(value):
        return True

    value = str(value).strip()

    if not expected_format:
        return True

    expected_format = str(expected_format).strip()

    if expected_format == "email":
        return re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            value,
        ) is not None

    if expected_format == "date":
        try:
            datetime.strptime(
                value,
                "%Y-%m-%d",
            )
            return True

        except ValueError:
            return False

    if expected_format == "datetime":
        try:
            datetime.fromisoformat(value)
            return True

        except ValueError:
            return False

    if expected_format.startswith("regex:"):
        pattern = expected_format[6:]

        try:
            return re.fullmatch(
                pattern,
                value,
            ) is not None

        except re.error:
            return False

    return True


def validate_format(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI FORMAT")
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
        expected_format = column_schema.get("format")

        if not expected_format:
            continue

        validated_columns += 1

        print("-" * 70)
        print(f"[DEBUG] Column              : {column_name}")
        print(f"[DEBUG] Expected format     : {expected_format}")

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

        invalid_rows = []

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if not _is_valid_format(
                value,
                expected_format,
            ):
                invalid_rows.append({
                    "row": row_number,
                    "value": value,
                })

        if invalid_rows:
            print(
                f"[DEBUG] Invalid values     : "
                f"{len(invalid_rows)}"
            )
            print(
                f"[DEBUG] Sample rows        : "
                f"{invalid_rows[:5]}"
            )
            print("[RESULT] Status            : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    f"{len(invalid_rows)} nilai "
                    f"tidak sesuai format."
                ),
                "invalid_rows": invalid_rows[:20],
            })

        else:
            print("[DEBUG] Invalid values     : 0")
            print("[RESULT] Status            : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": "Semua nilai sesuai format.",
            })

    if validated_columns == 0:
        print("[DEBUG] Tidak ada format rule dalam schema.")

    status = "FAIL" if failed_columns else "PASS"

    print("=" * 70)
    print("[RESULT] FORMAT VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Format validation berhasil."
            if status == "PASS"
            else "Terdapat nilai dengan format tidak sesuai."
        ),
        "details": details,
    }