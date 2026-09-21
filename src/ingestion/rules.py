import csv
import io
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import polars as pl

from .engine import sha256_file
from . import config


def check_source_files(train_path: Path, test_path: Path) -> Dict[str, Any]:
    info = {}
    for name, path in (("train", train_path), ("test", test_path)):
        if not path.exists():
            return {
                "status": "FAIL",
                "actual": f"{path} does not exist",
                "expected": "file exists",
                "message": f"Source file tidak ditemukan: {path}",
            }

        if not path.is_file():
            return {
                "status": "FAIL",
                "actual": f"{path} is not a regular file",
                "expected": "regular file",
                "message": f"Path bukan file: {path}",
            }

        if path.suffix.lower() != ".csv":
            return {
                "status": "FAIL",
                "actual": path.suffix.lower(),
                "expected": ".csv",
                "message": f"Source file harus CSV: {path}",
            }

        size_bytes = path.stat().st_size
        if size_bytes <= 0:
            return {
                "status": "FAIL",
                "actual": 0,
                "expected": "> 0 bytes",
                "message": f"Source file kosong: {path}",
            }

        info[name] = {
            "path": str(path),
            "file_name": path.name,
            "extension": path.suffix.lower(),
            "size_bytes": size_bytes,
        }

    return {
        "status": "PASS",
        "actual": info,
        "expected": "existing, non-empty .csv files",
        "message": "Source files exist and are valid CSV files.",
    }


def check_source_fingerprint(train_path: Path, test_path: Path) -> Dict[str, Any]:
    train_hash = sha256_file(train_path)
    test_hash = sha256_file(test_path)
    return {
        "status": "PASS",
        "actual": {"train_sha256": train_hash, "test_sha256": test_hash},
        "expected": "valid SHA-256 fingerprint",
        "message": "Source SHA-256 fingerprints generated successfully.",
    }


def check_csv_structure(path: Path) -> Dict[str, Any]:
    raw_bytes = path.read_bytes()
    if len(raw_bytes) == 0:
        return {
            "status": "FAIL",
            "actual": 0,
            "expected": "> 0 bytes",
            "message": f"CSV kosong: {path}",
        }

    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return {
            "status": "FAIL",
            "actual": str(exc),
            "expected": "utf-8 (or utf-8-sig) decodable",
            "message": f"{path} bukan UTF-8 compatible CSV: {exc}",
        }

    lines = text.splitlines()
    if len(lines) < 2:
        return {
            "status": "FAIL",
            "actual": len(lines),
            "expected": ">= 2 lines",
            "message": f"{path} harus memiliki header dan minimal satu data row",
        }

    header_line = lines[0]
    if "," not in header_line:
        return {
            "status": "FAIL",
            "actual": header_line,
            "expected": "comma-delimited header",
            "message": f"{path} tidak terlihat menggunakan delimiter ','",
        }

    header_columns = [
        column.strip().lower()
        for column in next(csv.reader(io.StringIO(header_line)))
    ]

    duplicate_columns = sorted({
        column for column in header_columns
        if header_columns.count(column) > 1
    })

    if duplicate_columns:
        return {
            "status": "FAIL",
            "actual": duplicate_columns,
            "expected": "no duplicate header columns",
            "message": f"{path} memiliki duplicate header: {duplicate_columns}",
        }

    return {
        "status": "PASS",
        "actual": {
            "encoding": "utf-8",
            "delimiter": ",",
            "line_count": len(lines),
            "header": header_columns,
        },
        "expected": "utf-8 CSV, comma-delimited, unique headers",
        "message": "CSV structural validation passed.",
    }


def load_raw_csv(path: Path) -> pl.DataFrame:
    return pl.read_csv(
        path,
        null_values=config.MISSING_VALUES,
        try_parse_dates=False,
        infer_schema_length=1000,
    )


def check_raw_load(train_path: Path, test_path: Path) -> Tuple[Dict[str, Any], Optional[pl.DataFrame], Optional[pl.DataFrame]]:
    try:
        train_df = load_raw_csv(train_path)
        test_df = load_raw_csv(test_path)
    except Exception as exc:
        return {
            "status": "FAIL",
            "actual": repr(exc),
            "expected": "CSV parses without error",
            "message": f"Gagal membaca CSV. Detail: {exc}",
        }, None, None

    return {
        "status": "PASS",
        "actual": {"train_shape": train_df.shape, "test_shape": test_df.shape},
        "expected": "non-empty dataframes",
        "message": "Raw CSV loaded successfully.",
    }, train_df, test_df


def normalize_column_names(df: pl.DataFrame) -> pl.DataFrame:
    normalized = [column.strip().lower() for column in df.columns]
    if len(normalized) != len(set(normalized)):
        duplicates = sorted({
            column for column in normalized
            if normalized.count(column) > 1
        })
        raise ValueError(f"Duplicate column names setelah normalisasi: {duplicates}")
    return df.rename(dict(zip(df.columns, normalized)))


def check_column_normalization(train_df: pl.DataFrame, test_df: pl.DataFrame) -> Tuple[Dict[str, Any], pl.DataFrame, pl.DataFrame]:
    try:
        norm_train = normalize_column_names(train_df)
        norm_test = normalize_column_names(test_df)
    except ValueError as exc:
        return {
            "status": "FAIL",
            "actual": str(exc),
            "expected": "no duplicate columns after lowercasing",
            "message": str(exc),
        }, train_df, test_df

    return {
        "status": "PASS",
        "actual": {"train_columns": norm_train.columns, "test_columns": norm_test.columns},
        "expected": "unique lowercase column names",
        "message": "Column names normalized to lowercase.",
    }, norm_train, norm_test


def check_columns(df: pl.DataFrame, expected_columns: List[str], dataset_name: str) -> Dict[str, Any]:
    if len(df.columns) != len(set(df.columns)):
        return {
            "status": "FAIL",
            "actual": df.columns,
            "expected": "unique column names",
            "message": f"{dataset_name}: duplicate column names",
        }

    if df.columns != expected_columns:
        return {
            "status": "FAIL",
            "actual": df.columns,
            "expected": expected_columns,
            "message": f"{dataset_name}: column schema tidak sesuai kontrak.",
        }

    return {
        "status": "PASS",
        "actual": df.columns,
        "expected": expected_columns,
        "message": f"{dataset_name} column schema matches the contract.",
    }


def schema_fingerprint(df: pl.DataFrame) -> str:
    schema_definition = [
        {"name": column, "dtype": str(dtype)}
        for column, dtype in df.schema.items()
    ]
    canonical_schema = json.dumps(schema_definition, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_schema.encode("utf-8")).hexdigest()


def check_dtypes(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    mismatches = {}
    for column, expected_dtype in config.EXPECTED_DTYPES.items():
        if column not in df.columns:
            continue
        actual_dtype = df.schema[column]
        if actual_dtype != expected_dtype:
            mismatches[column] = {"expected": str(expected_dtype), "actual": str(actual_dtype)}

    if mismatches:
        return {
            "status": "FAIL",
            "actual": mismatches,
            "expected": "all dtypes match SCHEMA_CONTRACT",
            "message": f"{dataset_name}: {len(mismatches)} kolom memiliki dtype tidak sesuai.",
        }

    return {
        "status": "PASS",
        "actual": {c: str(t) for c, t in df.schema.items()},
        "expected": {c: str(t) for c, t in config.EXPECTED_DTYPES.items()},
        "message": f"{dataset_name}: data types match the schema contract.",
    }


def check_nonzero_rows(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    if df.height <= 0:
        return {
            "status": "FAIL",
            "actual": df.height,
            "expected": "> 0",
            "message": f"{dataset_name} dataset kosong",
        }

    return {
        "status": "PASS",
        "actual": df.height,
        "expected": "> 0",
        "message": f"{dataset_name} has {df.height} rows.",
    }


def check_row_count_baseline(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    expected = config.REFERENCE_ROW_COUNTS.get(dataset_name)
    if expected is None:
        return {
            "status": "PASS",
            "actual": df.height,
            "expected": "no baseline configured",
            "message": f"Tidak ada baseline row count untuk {dataset_name}, dilewati.",
        }

    drift = abs(df.height - expected)
    if drift > config.ROW_COUNT_DRIFT_TOLERANCE:
        return {
            "status": "WARNING",
            "actual": df.height,
            "expected": expected,
            "message": (
                f"{dataset_name}: jumlah baris ({df.height}) berbeda dari baseline "
                f"referensi Titanic ({expected}). Periksa apakah file benar/tidak ter-subset."
            ),
        }

    return {
        "status": "PASS",
        "actual": df.height,
        "expected": expected,
        "message": f"{dataset_name} row count matches the known reference baseline.",
    }


def check_primary_key(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    column = "passengerid"
    issues = []

    null_count = df[column].null_count()
    if null_count > 0:
        issues.append(f"{null_count} null value(s)")

    unique_count = df[column].n_unique()
    if unique_count != df.height:
        issues.append(f"{df.height - unique_count} duplicate identifier(s)")

    min_value = df[column].min()
    if min_value is None or min_value <= 0:
        issues.append(f"non-positive min value ({min_value})")

    if issues:
        return {
            "status": "FAIL",
            "actual": issues,
            "expected": "unique, non-null, positive passengerid",
            "message": f"{dataset_name}.{column}: " + "; ".join(issues),
        }

    return {
        "status": "PASS",
        "actual": {"null_count": 0, "unique": True, "min_value": min_value},
        "expected": "unique, non-null, positive passengerid",
        "message": f"{dataset_name}.{column} primary key validation passed.",
    }


def check_full_row_duplicates(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    duplicate_count = int(df.is_duplicated().sum())
    if duplicate_count > 0:
        return {
            "status": "FAIL",
            "actual": duplicate_count,
            "expected": 0,
            "message": f"{dataset_name} memiliki {duplicate_count} full-row duplicate.",
        }

    return {
        "status": "PASS",
        "actual": 0,
        "expected": 0,
        "message": f"{dataset_name}: no full-row duplicates detected.",
    }


def check_business_key_duplicates(df: pl.DataFrame, dataset_name: str, keys=("name", "ticket")) -> Dict[str, Any]:
    available_keys = [k for k in keys if k in df.columns]

    if not available_keys:
        return {
            "status": "PASS",
            "actual": "no business key columns available",
            "expected": "n/a",
            "message": f"{dataset_name}: business-key check dilewati (kolom tidak tersedia).",
        }

    grouped = (
        df.group_by(available_keys)
        .agg(pl.len().alias("occurrences"), pl.col("passengerid").alias("passengerids"))
        .filter(pl.col("occurrences") > 1)
    )

    if grouped.height > 0:
        sample = grouped.head(10).to_dicts()
        return {
            "status": "WARNING",
            "actual": {"duplicate_groups": grouped.height, "sample": sample},
            "expected": "each (name, ticket) combination appears once",
            "message": (
                f"{dataset_name}: ditemukan {grouped.height} kombinasi "
                f"{available_keys} yang muncul lebih dari sekali (indikasi "
                f"entri ganda penumpang yang sama dengan passengerid berbeda)."
            ),
        }

    return {
        "status": "PASS",
        "actual": 0,
        "expected": 0,
        "message": f"{dataset_name}: no business-key ({available_keys}) duplicates detected.",
    }


def missing_report(df: pl.DataFrame) -> pl.DataFrame:
    if df.height == 0:
        return pl.DataFrame({
            "column": df.columns,
            "null_count": [0] * df.width,
            "null_ratio": [0.0] * df.width,
            "null_percent": [0.0] * df.width,
        })

    return (
        df.null_count()
        .transpose(include_header=True, header_name="column", column_names=["null_count"])
        .with_columns(
            (pl.col("null_count") / df.height).alias("null_ratio"),
            (pl.col("null_count") / df.height * 100).round(2).alias("null_percent"),
        )
    )


def check_required_non_null(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    required_columns = config.REQUIRED_NON_NULL[dataset_name]
    null_counts = df.select([
        pl.col(c).null_count().alias(c) for c in required_columns
    ]).to_dicts()[0]

    violations = {c: n for c, n in null_counts.items() if n > 0}

    if violations:
        return {
            "status": "FAIL",
            "actual": violations,
            "expected": "0 nulls in required columns",
            "message": f"{dataset_name}: kolom wajib memiliki null: {violations}",
        }

    return {
        "status": "PASS",
        "actual": {c: 0 for c in required_columns},
        "expected": "0 nulls in required columns",
        "message": f"{dataset_name}: required non-null validation passed.",
    }


def check_missingness_threshold(missing_df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    violations = []
    for row in missing_df.to_dicts():
        column = row["column"]
        threshold = config.MISSINGNESS_THRESHOLDS.get(column)
        if threshold is None:
            continue

        if row["null_ratio"] > threshold:
            violations.append({
                "column": column,
                "null_ratio": round(row["null_ratio"], 4),
                "threshold": threshold,
            })

    if violations:
        return {
            "status": "FAIL",
            "actual": violations,
            "expected": "null_ratio <= configured threshold per column",
            "message": f"{dataset_name}: {len(violations)} kolom melebihi threshold missingness.",
        }

    return {
        "status": "PASS",
        "actual": "within configured thresholds",
        "expected": "within configured thresholds",
        "message": f"{dataset_name}: missingness is within the configured project thresholds.",
    }


def check_string_quality(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    columns = [c for c in config.STRING_COLUMNS if c in df.columns]
    if not columns:
        return {"status": "PASS", "actual": {}, "expected": "n/a", "message": "No string columns to check."}

    exprs = []
    for c in columns:
        non_null = pl.col(c).is_not_null()
        exprs.append((non_null & (pl.col(c).str.len_chars() == 0)).sum().alias(f"{c}__empty"))
        exprs.append((non_null & (pl.col(c) != pl.col(c).str.strip_chars())).sum().alias(f"{c}__whitespace"))

    stats = df.select(exprs).to_dicts()[0]
    per_column = {}
    total_empty = 0
    total_whitespace = 0

    for c in columns:
        empty_count = int(stats[f"{c}__empty"])
        whitespace_count = int(stats[f"{c}__whitespace"])
        total_empty += empty_count
        total_whitespace += whitespace_count

        if empty_count > 0:
            status = "FAIL"
        elif whitespace_count > 0:
            status = "WARNING"
        else:
            status = "PASS"

        per_column[c] = {"empty_count": empty_count, "whitespace_count": whitespace_count, "status": status}

    if total_empty > 0:
        overall = "FAIL"
    elif total_whitespace > 0:
        overall = "WARNING"
    else:
        overall = "PASS"

    return {
        "status": overall,
        "actual": per_column,
        "expected": {"empty_strings": 0, "leading_trailing_whitespace": 0},
        "message": (
            f"{dataset_name}: string quality checked without modifying raw values "
            f"({total_empty} empty, {total_whitespace} whitespace issues)."
        ),
    }


def check_name_format(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    if "name" not in df.columns:
        return {"status": "PASS", "actual": "n/a", "expected": "n/a", "message": "Kolom name tidak tersedia."}

    malformed = df.filter(~pl.col("name").str.contains(","))
    if malformed.height > 0:
        return {
            "status": "WARNING",
            "actual": {"malformed_count": malformed.height, "sample_ids": malformed["passengerid"].head(10).to_list()},
            "expected": "'Last, Title. First' pattern (contains a comma)",
            "message": f"{dataset_name}: {malformed.height} nama tidak mengikuti pola standar.",
        }

    return {
        "status": "PASS",
        "actual": 0,
        "expected": 0,
        "message": f"{dataset_name}: all names follow the expected pattern.",
    }


def check_numeric_domains(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    columns = [c for c in config.NUMERIC_BOUNDS if c in df.columns]
    if not columns:
        return {"status": "PASS", "actual": {}, "expected": "n/a", "message": "No numeric columns to check."}

    exprs = []
    for c in columns:
        bounds = config.NUMERIC_BOUNDS[c]
        condition = pl.col(c).is_not_null()
        sub_conditions = []

        if bounds.get("min") is not None:
            sub_conditions.append(pl.col(c) < bounds["min"])
        if bounds.get("max") is not None:
            sub_conditions.append(pl.col(c) > bounds["max"])

        if not sub_conditions:
            continue

        invalid_condition = sub_conditions[0]
        for sc in sub_conditions[1:]:
            invalid_condition = invalid_condition | sc

        exprs.append((condition & invalid_condition).sum().alias(c))

    if not exprs:
        return {"status": "PASS", "actual": {}, "expected": "n/a", "message": "No bounded numeric columns to check."}

    stats = df.select(exprs).to_dicts()[0]
    violations = {c: int(n) for c, n in stats.items() if n > 0}

    if violations:
        return {
            "status": "FAIL",
            "actual": violations,
            "expected": "0 out-of-bound values per column",
            "message": f"{dataset_name}: kolom di luar domain numerik: {violations}",
        }

    return {
        "status": "PASS",
        "actual": {c: 0 for c in columns},
        "expected": "0 out-of-bound values",
        "message": f"{dataset_name}: numeric domain validation passed.",
    }


def check_categorical_domains(df: pl.DataFrame, dataset_name: str) -> Dict[str, Any]:
    columns = [c for c in config.ALLOWED_VALUES if c in df.columns]
    if not columns:
        return {"status": "PASS", "actual": {}, "expected": "n/a", "message": "No categorical columns to check."}

    exprs = [
        (pl.col(c).is_not_null() & ~pl.col(c).is_in(list(config.ALLOWED_VALUES[c]))).sum().alias(c)
        for c in columns
    ]

    stats = df.select(exprs).to_dicts()[0]
    violating_columns = [c for c, n in stats.items() if n > 0]

    if violating_columns:
        details = {}
        for c in violating_columns:
            observed = set(df[c].drop_nulls().unique().to_list())
            details[c] = sorted(observed - config.ALLOWED_VALUES[c])

        return {
            "status": "FAIL",
            "actual": details,
            "expected": {c: sorted(config.ALLOWED_VALUES[c]) for c in columns},
            "message": f"{dataset_name}: nilai di luar domain kategorikal.",
        }

    return {
        "status": "PASS",
        "actual": {c: 0 for c in columns},
        "expected": "0 out-of-domain values",
        "message": f"{dataset_name}: categorical domain validation passed.",
    }