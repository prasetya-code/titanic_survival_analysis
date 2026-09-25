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


def validate_pattern(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI FORMAT")
    print("=" * 70)
    print(f"[DEBUG] Dataset              : {dataset_name}")
    print(f"[DEBUG] File                 : {file_path}")
    print(f"[DEBUG] Schema columns       : {len(schema)}")

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
            "invalid_count": 0,
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
    format_rules = 0
    total_invalid = 0

    for column_name, column_schema in schema.items():
        expected_format = column_schema.get("format")

        if not expected_format:
            continue

        format_rules += 1
        validated_columns += 1

        print("-" * 70)
        print(f"[DEBUG] Column              : {column_name}")
        print(f"[DEBUG] Expected format     : {expected_format}")

        actual_column = csv_columns.get(column_name.strip().casefold())

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print("[RESULT] Status            : FAIL")

            failed_columns.append(column_name)
            total_invalid += 1
            details.append({
                "column": column_name,
                "status": "FAIL",
                "invalid_count": 1,
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
            total_invalid += len(invalid_rows)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "invalid_count": len(invalid_rows),
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
                "invalid_count": 0,
                "message": "Semua nilai sesuai format.",
            })

    print(f"[DEBUG] Format rules         : {format_rules}")
    print(f"[DEBUG] Validated columns    : {validated_columns}")

    if validated_columns == 0:
        print("\t [DEBUG] Tidak ada format rule dalam schema.")
        print("[RESULT] Validation status  : SKIPPED \n")

        status = "SKIPPED"
        message = "Tidak ada format rule dalam schema."

    elif failed_columns:
        status = "FAIL"
        message = "Terdapat nilai dengan format tidak sesuai."

    else:
        status = "PASS"
        message = "Format validation berhasil."

    print("=" * 70)
    print("[RESULT] FORMAT VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "invalid_count": total_invalid,
        "message": message,
        "details": details,
    }


""" Dengan schema Titanic Anda yang **tidak memiliki `format`**, output sekarang akan menjadi:

```text
======================================================================
[INFO] VALIDASI FORMAT
======================================================================
[DEBUG] Dataset              : train
[DEBUG] File                 : d:\GIT DATA\titanic_survival_analysis\data\raw\train.csv
[DEBUG] Schema columns       : 12
[DEBUG] CSV columns          : 12
[DEBUG] Data rows            : 891
[DEBUG] Format rules         : 0
[DEBUG] Validated columns    : 0
[DEBUG] Tidak ada format rule dalam schema.
[RESULT] Validation status  : SKIPPED
======================================================================
[RESULT] FORMAT VALIDATION
======================================================================
[RESULT] Dataset             : train
[RESULT] Status              : SKIPPED
```

Dan hasil return-nya:

```python
{
    "status": "SKIPPED",
    "invalid_count": 0,
    "message": "Tidak ada format rule dalam schema.",
    "details": []
}
```

Sedangkan jika nanti schema memiliki:

```json
"email": {
    "dtype": "String",
    "format": "email",
    "nullable": false,
    "required": true
}
```

dan seluruh 891 baris valid, hasilnya:

```text
[DEBUG] Format rules         : 1
[DEBUG] Validated columns    : 1
----------------------------------------------------------------------
[DEBUG] Column              : email
[DEBUG] Expected format     : email
[DEBUG] Invalid values      : 0
[RESULT] Status             : PASS
======================================================================
[RESULT] FORMAT VALIDATION
======================================================================
[RESULT] Dataset             : train
[RESULT] Status              : PASS
```

Jadi sekarang makna statusnya konsisten:

```text
PASS    = rule ada + data lolos
FAIL    = rule ada + data melanggar
SKIPPED = tidak ada rule
ERROR   = proses validasi gagal secara teknis
```

Ini lebih tepat untuk dijadikan salah satu komponen **ingestion validation report** Anda.
 """