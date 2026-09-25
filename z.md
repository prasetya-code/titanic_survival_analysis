```py
MISSING_VALUES = ["", "NA", "N/A", "na", "n/a", "N/a"]
```

```bash
DQ-005
Data Quality Validation
│
├── Completeness
│   ├── Missing Value Profiling
│   └── Missingness Threshold
│
├── Uniqueness
│   ├── Primary Key
│   ├── Full-Row Duplicate
│   └── Business-Key Duplicate
│
├── Validity
│   ├── String Quality
│   ├── Name Format
│   ├── Numeric Domain
│   └── Categorical Domain
│
├── Integrity
│   └── Row Count / Baseline Drift
│
└── Consistency
    └── Train / Test Relationship


DQ-006
Staged Artifact Validation
│
├── Parquet Read-back
├── Schema Match
└── Artifact Integrity


DQ-007
Provenance & Audit Validation
│
├── Run Metadata
├── Git Commit
├── Environment
└── Validation Report
```











- `validasi unique` seharusnya melakukan cek full row duplication serta business key duplication