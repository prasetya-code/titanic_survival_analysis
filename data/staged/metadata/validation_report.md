# Ingestion Validation Report — `titanic-ingestion-20260917T055224Z`

- **Dataset**: titanic
- **Timestamp (UTC)**: 2026-09-17T05:52:24.034203+00:00
- **Overall status**: **PASS_WITH_WARNINGS**
- **Duration**: 2.4074s

| Total | Passed | Warnings | Failed | Errored |
|---|---|---|---|---|
| 36 | 34 | 2 | 0 | 0 |

## Rule Detail

| Rule | Check | Dataset | Severity | Status | Message |
|---|---|---|---|---|---|
| DQ-001 | source_files | all | CRITICAL | PASS | Source files exist and are valid CSV files. |
| DQ-002 | source_fingerprint | all | CRITICAL | PASS | Source SHA-256 fingerprints generated successfully. |
| DQ-003 | csv_structure | train | CRITICAL | PASS | CSV structural validation passed. |
| DQ-003 | csv_structure | test | CRITICAL | PASS | CSV structural validation passed. |
| DQ-004 | raw_load | all | CRITICAL | PASS | Raw CSV loaded successfully. |
| DQ-005 | column_normalization | all | CRITICAL | PASS | Column names normalized to lowercase. |
| DQ-006 | column_schema | train | CRITICAL | PASS | train column schema matches the contract. |
| DQ-007 | column_schema | test | CRITICAL | PASS | test column schema matches the contract. |
| DQ-008 | data_types | train | CRITICAL | PASS | train: data types match the schema contract. |
| DQ-008 | data_types | test | CRITICAL | PASS | test: data types match the schema contract. |
| DQ-009 | row_count_nonzero | train | CRITICAL | PASS | train has 891 rows. |
| DQ-009 | row_count_nonzero | test | CRITICAL | PASS | test has 418 rows. |
| DQ-010 | row_count_baseline | train | WARNING | PASS | train row count matches the known reference baseline. |
| DQ-010 | row_count_baseline | test | WARNING | PASS | test row count matches the known reference baseline. |
| DQ-011 | primary_key | train | CRITICAL | PASS | train.passengerid primary key validation passed. |
| DQ-011 | primary_key | test | CRITICAL | PASS | test.passengerid primary key validation passed. |
| DQ-012 | full_row_duplicates | train | CRITICAL | PASS | train: no full-row duplicates detected. |
| DQ-012 | full_row_duplicates | test | CRITICAL | PASS | test: no full-row duplicates detected. |
| DQ-013 | business_key_duplicates | train | WARNING | PASS | train: no business-key (['name', 'ticket']) duplicates detected. |
| DQ-013 | business_key_duplicates | test | WARNING | PASS | test: no business-key (['name', 'ticket']) duplicates detected. |
| DQ-014 | required_non_null | train | CRITICAL | PASS | train: required non-null validation passed. |
| DQ-014 | required_non_null | test | CRITICAL | PASS | test: required non-null validation passed. |
| DQ-015 | missingness_threshold | train | CRITICAL | PASS | train: missingness is within the configured project thresholds. |
| DQ-015 | missingness_threshold | test | CRITICAL | PASS | test: missingness is within the configured project thresholds. |
| DQ-016 | string_quality | train | WARNING | WARNING | train: string quality checked without modifying raw values (0 empty, 2 whitespace issues). |
| DQ-016 | string_quality | test | WARNING | WARNING | test: string quality checked without modifying raw values (0 empty, 2 whitespace issues). |
| DQ-017 | name_format | train | WARNING | PASS | train: all names follow the expected pattern. |
| DQ-017 | name_format | test | WARNING | PASS | test: all names follow the expected pattern. |
| DQ-018 | numeric_domain | train | CRITICAL | PASS | train: numeric domain validation passed. |
| DQ-018 | numeric_domain | test | CRITICAL | PASS | test: numeric domain validation passed. |
| DQ-019 | categorical_domain | train | CRITICAL | PASS | train: categorical domain validation passed. |
| DQ-019 | categorical_domain | test | CRITICAL | PASS | test: categorical domain validation passed. |
| DQ-020 | train_test_relationship | all | CRITICAL | PASS | Train and test passenger IDs do not overlap. |
| DQ-021 | staged_write | all | CRITICAL | PASS | Staged Parquet artifacts created successfully. |
| DQ-022 | staged_readback | all | CRITICAL | PASS | Staged artifacts readable and structurally valid. |
| DQ-023 | staged_schema_fingerprint | all | CRITICAL | PASS | Staged schema fingerprints match source schema. |
