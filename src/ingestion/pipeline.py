import json
from pathlib import Path
from typing import Tuple, Dict, Any
import polars as pl

from . import config
from . import rules
from .engine import run_rule


def run_ingestion_pipeline(
    train_path: Path = Path(config.TRAIN_RAW),
    test_path: Path = Path(config.TEST_RAW),
    history_dir: Path = Path(config.HISTORY_DIR)
) -> Tuple[pl.DataFrame, pl.DataFrame, Dict[str, Any]]:
    
    # DQ-001 — Source File Validation
    run_rule("DQ-001", "source_files", "all", "CRITICAL", True, rules.check_source_files, train_path, test_path, history_dir=history_dir)

    # DQ-002 — Source Fingerprint (SHA-256)
    fp_check = run_rule("DQ-002", "source_fingerprint", "all", "CRITICAL", False, rules.check_source_fingerprint, train_path, test_path, history_dir=history_dir)
    fp_data = json.loads(fp_check["actual"])
    print(f"\nTrain SHA256: {fp_data['train_sha256']}")
    print(f"Test  SHA256: {fp_data['test_sha256']}")

    # DQ-003 — CSV Structural Validation
    run_rule("DQ-003", "csv_structure", "train", "CRITICAL", True, rules.check_csv_structure, train_path, history_dir=history_dir)
    run_rule("DQ-003", "csv_structure", "test", "CRITICAL", True, rules.check_csv_structure, test_path, history_dir=history_dir)

    # DQ-004 — Raw Data Loading
    load_res, train_df, test_df = rules.check_raw_load(train_path, test_path)
    run_rule("DQ-004", "raw_load", "all", "CRITICAL", True, lambda: load_res, history_dir=history_dir)

    print(f"Train shape: {train_df.shape}")
    print(f"Test shape : {test_df.shape}")

    # DQ-005 — Technical Column Name Standardization
    norm_res, train_df, test_df = rules.check_column_normalization(train_df, test_df)
    run_rule("DQ-005", "column_normalization", "all", "CRITICAL", True, lambda: norm_res, history_dir=history_dir)

    # DQ-006 & DQ-007 — Column Schema Validation
    run_rule("DQ-006", "column_schema", "train", "CRITICAL", True, rules.check_columns, train_df, config.EXPECTED_TRAIN_COLUMNS, "train", history_dir=history_dir)
    run_rule("DQ-007", "column_schema", "test", "CRITICAL", True, rules.check_columns, test_df, config.EXPECTED_TEST_COLUMNS, "test", history_dir=history_dir)

    print("Train schema SHA256:", rules.schema_fingerprint(train_df))
    print("Test  schema SHA256:", rules.schema_fingerprint(test_df))

    # DQ-008 — Data Type Validation
    run_rule("DQ-008", "data_types", "train", "CRITICAL", True, rules.check_dtypes, train_df, "train", history_dir=history_dir)
    run_rule("DQ-008", "data_types", "test", "CRITICAL", True, rules.check_dtypes, test_df, "test", history_dir=history_dir)

    # DQ-009 — Row Count Sanity
    run_rule("DQ-009", "row_count_nonzero", "train", "CRITICAL", True, rules.check_nonzero_rows, train_df, "train", history_dir=history_dir)
    run_rule("DQ-009", "row_count_nonzero", "test", "CRITICAL", True, rules.check_nonzero_rows, test_df, "test", history_dir=history_dir)

    # DQ-010 — Row Count Baseline Drift
    run_rule("DQ-010", "row_count_baseline", "train", "WARNING", False, rules.check_row_count_baseline, train_df, "train", history_dir=history_dir)
    run_rule("DQ-010", "row_count_baseline", "test", "WARNING", False, rules.check_row_count_baseline, test_df, "test", history_dir=history_dir)

    # DQ-011 — Primary Key Validation
    run_rule("DQ-011", "primary_key", "train", "CRITICAL", False, rules.check_primary_key, train_df, "train", history_dir=history_dir)
    run_rule("DQ-011", "primary_key", "test", "CRITICAL", False, rules.check_primary_key, test_df, "test", history_dir=history_dir)

    # DQ-012 — Full-Row Duplicate
    run_rule("DQ-012", "full_row_duplicates", "train", "CRITICAL", False, rules.check_full_row_duplicates, train_df, "train", history_dir=history_dir)
    run_rule("DQ-012", "full_row_duplicates", "test", "CRITICAL", False, rules.check_full_row_duplicates, test_df, "test", history_dir=history_dir)

    # DQ-013 — Business-Key Duplicate
    run_rule("DQ-013", "business_key_duplicates", "train", "WARNING", False, rules.check_business_key_duplicates, train_df, "train", history_dir=history_dir)
    run_rule("DQ-013", "business_key_duplicates", "test", "WARNING", False, rules.check_business_key_duplicates, test_df, "test", history_dir=history_dir)

    # Profiling & Missingness Checks
    train_missing = rules.missing_report(train_df)
    test_missing = rules.missing_report(test_df)

    # DQ-014 — Required Non-Null
    run_rule("DQ-014", "required_non_null", "train", "CRITICAL", False, rules.check_required_non_null, train_df, "train", history_dir=history_dir)
    run_rule("DQ-014", "required_non_null", "test", "CRITICAL", False, rules.check_required_non_null, test_df, "test", history_dir=history_dir)

    # DQ-015 — Missingness Threshold
    run_rule("DQ-015", "missingness_threshold", "train", "CRITICAL", False, rules.check_missingness_threshold, train_missing, "train", history_dir=history_dir)
    run_rule("DQ-015", "missingness_threshold", "test", "CRITICAL", False, rules.check_missingness_threshold, test_missing, "test", history_dir=history_dir)

    # DQ-016 — String Quality
    run_rule("DQ-016", "string_quality", "train", "WARNING", False, rules.check_string_quality, train_df, "train", history_dir=history_dir)
    run_rule("DQ-016", "string_quality", "test", "WARNING", False, rules.check_string_quality, test_df, "test", history_dir=history_dir)

    # DQ-017 — Name Format
    run_rule("DQ-017", "name_format", "train", "WARNING", False, rules.check_name_format, train_df, "train", history_dir=history_dir)
    run_rule("DQ-017", "name_format", "test", "WARNING", False, rules.check_name_format, test_df, "test", history_dir=history_dir)

    # DQ-018 — Numeric Domain
    run_rule("DQ-018", "numeric_domain", "train", "CRITICAL", False, rules.check_numeric_domains, train_df, "train", history_dir=history_dir)
    run_rule("DQ-018", "numeric_domain", "test", "CRITICAL", False, rules.check_numeric_domains, test_df, "test", history_dir=history_dir)

    # DQ-019 — Categorical Domain
    run_rule("DQ-019", "categorical_domain", "train", "CRITICAL", False, rules.check_categorical_domains, train_df, "train", history_dir=history_dir)
    run_rule("DQ-019", "categorical_domain", "test", "CRITICAL", False, rules.check_categorical_domains, test_df, "test", history_dir=history_dir)

    reports = {
        "train_missing": train_missing,
        "test_missing": test_missing,
    }

    return train_df, test_df, reports