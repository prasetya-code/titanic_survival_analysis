from config import *
from datetime import datetime

import csv
import json
import math
import yaml


# File
INPUT_FILE = TRAIN_RAW
SCHEMA_FILE = SCHEMA_CONTRACT
OUTPUT_FILE = BASELINE_PROFILE


def _is_null(value):

    if value is None:

        return True

    value = str(value).strip().casefold()

    return value in {
        "",
        "null",
        "none",
        "nan",
        "n/a",
    }


def create_baseline_profile():

    print("=" * 60)
    print("START: Baseline Profiling")
    print("=" * 60)

    try:
        # --------------------------------------------------
        # 1. Debug project location & setup parameters
        # --------------------------------------------------
        print(f"[DEBUG] ROOT_PROJECT (CWD) : {ROOT_PROJECT}")
        print(f"[DEBUG] Dataset Name       : {PROJECT_NAME}")
        print(f"[DEBUG] Input File         : {INPUT_FILE}")
        print(f"[DEBUG] Schema File        : {SCHEMA_FILE}")
        print(f"[DEBUG] Output File        : {OUTPUT_FILE}")

        # --------------------------------------------------
        # 2. Read Schema from YAML file
        # --------------------------------------------------
        print("[INFO] Checking schema YAML file existence...")

        if not SCHEMA_FILE.exists():

            raise FileNotFoundError(
                f"Schema YAML file not found: {SCHEMA_FILE}"
            )

        print("[INFO] Loading schema from YAML file...")

        with open(
            SCHEMA_FILE,
            "r",
            encoding="utf-8",
        ) as yaml_file:

            schema_data = yaml.safe_load(yaml_file) or {}

        # Ambil dictionary kolom dari root key 'columns'
        schema_columns = schema_data.get("columns", {})

        if not schema_columns:

            raise ValueError(
                "Key 'columns' tidak ditemukan atau kosong di dalam file YAML."
            )

        print(f"[DEBUG] Schema columns count : {len(schema_columns)}")

        # --------------------------------------------------
        # 3. Check and Read CSV file
        # --------------------------------------------------
        print("[INFO] Checking input file existence...")

        if not INPUT_FILE.exists():

            raise FileNotFoundError(
                f"CSV input file not found: {INPUT_FILE}"
            )

        print("[INFO] Reading CSV file...")

        with open(
            INPUT_FILE,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            reader = csv.DictReader(file)

            fieldnames = reader.fieldnames or []
            rows = list(reader)

        print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
        print(f"[DEBUG] Data rows            : {len(rows)}")

        csv_columns = {
            column.strip().casefold(): column
            for column in fieldnames
        }

        # --------------------------------------------------
        # 4. Initialize dataset profile
        # --------------------------------------------------
        profile = {
            "dataset": PROJECT_NAME,
            "source_file": str(INPUT_FILE),
            "schema_file": str(SCHEMA_FILE),
            "created_at": datetime.now().isoformat(),
            "row_count": len(rows),
            "column_count": len(fieldnames),
            "columns": {},
        }

        details = []

        # --------------------------------------------------
        # 5. Column profiling
        # --------------------------------------------------
        for column_name, column_schema in schema_columns.items():

            print("-" * 60)
            print(f"[DEBUG] Processing Column : {column_name}")

            actual_column = csv_columns.get(
                column_name.strip().casefold()
            )

            # Check column existence
            if actual_column is None:

                print("[INFO] Column status     : SKIP (Not found in CSV)")

                details.append({
                    "column": column_name,
                    "status": "SKIP",
                    "message": "Column tidak ditemukan di CSV.",
                })

                continue

            print(f"[DEBUG] Actual column     : {actual_column}")

            dtype = str(
                column_schema.get("dtype", "")
            ).casefold()

            semantic_type = str(
                column_schema.get("semantic_type", "")
            ).casefold()

            null_count = 0
            non_null_count = 0
            values = []

            # Extract column values
            for row in rows:

                value = row.get(actual_column)

                if _is_null(value):

                    null_count += 1

                else:

                    non_null_count += 1

                    values.append(str(value).strip())

            # Calculate basic statistics
            row_count = len(rows)

            if row_count > 0:

                null_rate = null_count / row_count
                non_null_rate = non_null_count / row_count

            else:

                null_rate = 0.0
                non_null_rate = 0.0

            unique_values = set(values)
            unique_count = len(unique_values)

            if non_null_count > 0:

                unique_rate = unique_count / non_null_count

            else:

                unique_rate = 0.0

            column_profile = {
                "dtype": column_schema.get("dtype"),
                "semantic_type": column_schema.get("semantic_type"),
                "row_count": row_count,
                "null_count": null_count,
                "non_null_count": non_null_count,
                "null_rate": round(null_rate, 6),
                "non_null_rate": round(non_null_rate, 6),
                "unique_count": unique_count,
                "unique_rate": round(unique_rate, 6),
            }

            # Numerical profile
            numerical_types = {
                "int",
                "integer",
                "int64",
                "float",
                "float64",
                "number",
                "numeric",
            }

            if dtype in numerical_types or semantic_type in {"numeric", "count"}:

                numeric_values = []

                for value in values:

                    try:

                        numeric_value = float(value)

                        if math.isfinite(numeric_value):

                            numeric_values.append(numeric_value)

                    except (ValueError, TypeError):

                        continue

                if numeric_values:

                    numeric_values.sort()

                    count = len(numeric_values)
                    mean = sum(numeric_values) / count
                    variance = (
                        sum((val - mean) ** 2 for val in numeric_values)
                        / count
                    )
                    std = math.sqrt(variance)

                    column_profile["statistics"] = {
                        "count": count,
                        "min": min(numeric_values),
                        "max": max(numeric_values),
                        "mean": round(mean, 6),
                        "std": round(std, 6),
                        "median": round(numeric_values[count // 2], 6),
                    }

                    print("[SUCCESS] Numeric profile : PASS")

                else:

                    column_profile["statistics"] = {}

                    print("[INFO] Numeric profile    : SKIP (No valid numeric data)")

            # Categorical profile
            categorical_types = {
                "categorical",
                "binary",
                "binary_target",
            }

            if semantic_type in categorical_types:

                value_counts = {}

                for value in values:

                    normalized_value = str(value).strip().casefold()

                    value_counts[normalized_value] = (
                        value_counts.get(normalized_value, 0) + 1
                    )

                distribution = {}

                for val, count in value_counts.items():

                    distribution[val] = round(count / non_null_count, 6)

                column_profile["distribution"] = distribution

                print("[SUCCESS] Categorical profile : PASS")

            # Allowed values rule
            allowed_values = column_schema.get("allowed_values")

            if allowed_values is not None:

                column_profile["allowed_values"] = allowed_values

            # Save column result
            profile["columns"][column_name] = column_profile

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": "Baseline profile berhasil dibuat.",
            })

        # --------------------------------------------------
        # 6. Save baseline profile to JSON
        # --------------------------------------------------
        print("=" * 60)
        print("[INFO] Creating output directory if needed...")

        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        print("[INFO] Saving baseline profile...")

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False,
            )

        print(f"[SUCCESS] Profile saved to: {OUTPUT_FILE}")

        # --------------------------------------------------
        # 7. Final Result Summary
        # --------------------------------------------------
        print("=" * 60)
        print("SUCCESS: Baseline profiling completed.")
        print("=" * 60)

        print(f"[SUCCESS] Dataset   : {PROJECT_NAME}")
        print(f"[SUCCESS] Rows      : {len(rows)}")
        print(f"[SUCCESS] Columns   : {len(fieldnames)}")
        print(f"[SUCCESS] Output    : {OUTPUT_FILE}")

        return {
            "status": "PASS",
            "message": "Baseline profiling berhasil.",
            "profile": profile,
            "details": details,
        }

    except FileNotFoundError as error:

        print("=" * 60)
        print("[ERROR] File or directory not found.")
        print("=" * 60)

        print(f"[ERROR] {error}")

        return {
            "status": "ERROR",
            "message": f"File tidak ditemukan: {error}",
            "details": [],
        }

    except Exception as error:

        print("=" * 60)
        print("[ERROR] Unexpected error during baseline profiling.")
        print("=" * 60)

        print(f"[ERROR TYPE] {type(error).__name__}")
        print(f"[ERROR] {error}")

        return {
            "status": "ERROR",
            "message": f"Gagal memproses baseline profile: {error}",
            "details": details if "details" in locals() else [],
        }

    finally:

        print("=" * 60)
        print("END: Baseline Profiling")
        print("=" * 60)


if __name__ == "__main__":
    create_baseline_profile()