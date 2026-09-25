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


def validate_duplication(
    file_path,
    dataset_name,
    schema,
    business=None,
):
    print("=" * 70)
    print("[INFO] VALIDASI UNIQUE")
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
            "message": f"Gagal membaca CSV: {error}",
            "details": [],
        }

    csv_columns = {
        column.strip().casefold(): column
        for column in fieldnames
    }

    print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
    print(f"[DEBUG] Data rows            : {len(rows)}")
    print(f"{'-' * 70} \n")

    details = []
    failed_checks = []

    # ================================================================
    # FULL ROW DUPLICATION
    # ================================================================

    print("[DEBUG] Validasi            : Full Row Duplication")

    row_values = defaultdict(list)

    for index, row in enumerate(rows):

        row_key = tuple(
            str(row.get(column, "")).strip()
            for column in fieldnames
        )

        row_values[row_key].append(index)

    duplicate_rows = {
        row_key: indexes
        for row_key, indexes in row_values.items()
        if len(indexes) > 1
    }

    duplicate_row_count = len(duplicate_rows)

    print(f"[DEBUG] Duplicate rows      : {duplicate_row_count}")

    if duplicate_rows:

        print("[DEBUG] Sample duplicates   :")

        for row_key, indexes in list(
            duplicate_rows.items()
        )[:5]:

            csv_rows = [
                index + 2
                for index in indexes
            ]

            print(f"CSV Rows    : {csv_rows}")
            print(f"Index       : {indexes}")
            print(f"Value       : {row_key}")

        print("[RESULT] Status             : FAIL")

        failed_checks.append("full_row")

        details.append({
            "type": "full_row",
            "status": "FAIL",
            "message": (
                f"Ditemukan {duplicate_row_count} "
                "duplicate full row."
            ),
            "duplicates": {
                row_key: {
                    "index": indexes,
                    "rows": [
                        index + 2
                        for index in indexes
                    ],
                }
                for row_key, indexes in list(
                    duplicate_rows.items()
                )[:20]
            },
        })

    else:

        print("[RESULT] Status             : PASS")

        details.append({
            "type": "full_row",
            "status": "PASS",
            "message": "Tidak ditemukan duplicate full row.",
        })

    print(f"{'-' * 70} \n")
    

    # ================================================================
    # BUSINESS KEY / COMPOSITE UNIQUENESS
    # ================================================================

    business_rules = []

    if business:
        business_rules = business.get("unique", [])

    print("-" * 70)
    print(f"[DEBUG] Business rules      : {len(business_rules)}")

    for business_rule in business_rules:

        business_name = business_rule.get("name")
        business_columns = business_rule.get("columns", [])

        print(f"{'-' * 70} \n")

        print(f"[DEBUG] Business key        : {business_name}")
        print(f"[DEBUG] Columns             : {business_columns}")

        actual_business_columns = []

        for column_name in business_columns:

            actual_column = csv_columns.get(
                column_name.strip().casefold()
            )

            if actual_column is None:

                print(
                    f"[DEBUG] Column              : "
                    f"{column_name}"
                )
                print(
                    "[DEBUG] Actual column       : "
                    "NOT FOUND"
                )
                print("[RESULT] Status             : FAIL")

                failed_checks.append(
                    f"business:{business_name}"
                )

                details.append({
                    "type": "business",
                    "name": business_name,
                    "columns": business_columns,
                    "status": "FAIL",
                    "message": (
                        f"Kolom '{column_name}' "
                        "tidak ditemukan di CSV."
                    ),
                })

                actual_business_columns = []
                break

            actual_business_columns.append(
                actual_column
            )

        if not actual_business_columns:
            continue

        business_values = defaultdict(list)

        for index, row in enumerate(rows):

            if all(
                _is_null(row.get(column))
                for column in actual_business_columns
            ):
                continue

            business_key = tuple(
                str(row.get(column, "")).strip()
                for column in actual_business_columns
            )

            business_values[business_key].append(index)

        business_duplicates = {
            business_key: indexes
            for business_key, indexes
            in business_values.items()
            if len(indexes) > 1
        }

        duplicate_business_count = len(
            business_duplicates
        )

        print(
            f"[DEBUG] Duplicate values    : "
            f"{duplicate_business_count}"
        )

        if business_duplicates:

            print("[DEBUG] Sample duplicates   :")

            for business_key, indexes in list(
                business_duplicates.items()
            )[:5]:

                csv_rows = [
                    index + 2
                    for index in indexes
                ]

                print(f"CSV Rows    : {csv_rows}")
                print(f"Index       : {indexes}")
                print(f"Value       : {business_key} \n")

            print("[RESULT] Status             : FAIL")

            failed_checks.append(
                f"business:{business_name}"
            )

            details.append({
                "type": "business",
                "name": business_name,
                "columns": business_columns,
                "status": "FAIL",
                "message": (
                    f"Ditemukan {duplicate_business_count} "
                    "duplicate business key."
                ),
                "duplicates": {
                    business_key: {
                        "index": indexes,
                        "rows": [
                            index + 2
                            for index in indexes
                        ],
                    }
                    for business_key, indexes in list(
                        business_duplicates.items()
                    )[:20]
                },
            })

        else:

            print("[RESULT] Status             : PASS")

            details.append({
                "type": "business",
                "name": business_name,
                "columns": business_columns,
                "status": "PASS",
                "message": (
                    "Semua business key unique."
                ),
            })

    if not business_rules:

        print(
            "[DEBUG] Tidak ada business "
            "unique rule."
        )

    status = "FAIL" if failed_checks else "PASS"

    print(f"\n{'=' * 70}")
    print("[RESULT] UNIQUE VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Unique validation berhasil."
            if status == "PASS"
            else "Terdapat duplicate data."
        ),
        "details": details,
    }
