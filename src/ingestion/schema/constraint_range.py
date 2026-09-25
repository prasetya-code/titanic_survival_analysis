import csv


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


def validate_range(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI CONSTRAINT")
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
    failed_columns = []
    validated_columns = 0

    for column_name, column_schema in schema.items():
        minimum = column_schema.get("min")
        maximum = column_schema.get("max")

        if minimum is None and maximum is None:
            continue

        validated_columns += 1

        print(f"[DEBUG] Column              : {column_name}")
        print(f"[DEBUG] Min                 : {minimum}")
        print(f"[DEBUG] Max                 : {maximum}")

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": "Kolom tidak ditemukan di CSV.",
            })

            continue

        invalid_rows = []
        skipped_rows = 0

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if _is_null(value):
                skipped_rows += 1
                continue

            try:
                numeric_value = float(value)

            except (ValueError, TypeError):
                invalid_rows.append({
                    "row": row_number,
                    "value": value,
                    "reason": "Bukan nilai numerik.",
                })
                continue

            if minimum is not None and numeric_value < float(minimum):
                invalid_rows.append({
                    "row": row_number,
                    "value": value,
                    "reason": f"< min ({minimum})",
                })
                continue

            if maximum is not None and numeric_value > float(maximum):
                invalid_rows.append({
                    "row": row_number,
                    "value": value,
                    "reason": f"> max ({maximum})",
                })            

        print(f"[DEBUG] Invalid values      : {len(invalid_rows)}")
        # print(f"[DEBUG] Skipped null        : {skipped_rows}")

        if invalid_rows:
            print(
                f"[DEBUG] Sample rows        : "
                f"{invalid_rows[:5]}"
            )
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    f"{len(invalid_rows)} nilai "
                    f"melanggar constraint."
                ),
                "invalid_rows": invalid_rows[:20],
            })

        else:
            print("[RESULT] Status             : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": "Semua nilai memenuhi constraint.",
            })

        print(f"{'-' * 70} \n")
        

    if validated_columns == 0:
        print("[DEBUG] Tidak ada constraint min/max.")
    

    status = "FAIL" if failed_columns else "PASS"

    print("=" * 70)
    print("[RESULT] CONSTRAINT VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Constraint validation berhasil."
            if status == "PASS"
            else "Terdapat nilai yang melanggar constraint."
        ),
        "details": details,
    }