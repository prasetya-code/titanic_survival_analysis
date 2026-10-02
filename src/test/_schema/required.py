import csv


def validate_required(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI REQUIRED COLUMN")
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

    for column_name, column_schema in schema.items():
        required = column_schema.get("required")

        if required is not True:
            continue

        print(f"[DEBUG] Required column     : {column_name}")

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        if actual_column is None:
            print("[DEBUG] Column status       : MISSING")
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": "Required column tidak ditemukan.",
            })

        else:
            print(
                f"[DEBUG] Actual column       : "
                f"{actual_column}"
            )
            print("[DEBUG] Column status       : FOUND")
            print("[RESULT] Status             : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": "Required column ditemukan.",
            })

        print(f"{'-' * 70} \n")
        

    if not details:
        print("[DEBUG] Tidak ada required column.")

    status = "FAIL" if failed_columns else "PASS"

    print("=" * 70)
    print("[RESULT] REQUIRED VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Required column validation berhasil."
            if status == "PASS"
            else "Terdapat required column yang tidak ditemukan."
        ),
        "details": details,
    }