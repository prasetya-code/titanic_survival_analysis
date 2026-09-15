# Tujuan

Pipeline production harus:

* reproducible
* predictable
* observable
* memory-aware
* error-tolerant
* mudah di-maintain

---

# Arsitektur

Untuk dataset besar:

```bash
                ┌──────────────┐
                │   Database   │
                └──────┬───────┘
                       ↓
                  SQL Filter
                       ↓
                    Batch
                       ↓
              ┌────────────────┐
              │     Polars     │
              │     Lazy       │
              └───────┬────────┘
                      ↓
                 Transform
                      ↓
                 Validation
                      ↓
                 Parquet
                      ↓
                 Partition
```

---

# Folder Production

Contoh:

```bash
project/
│
├── data/
│   ├── raw/
│   ├── staging/
│   └── processed/
│
├── src/
│   ├── ingestion.py
│   ├── transform.py
│   ├── validation.py
│   └── pipeline.py
│
├── logs/
│
└── tests/
```

---

# Input

Jangan langsung memproses data tanpa validasi. Periksa:

```python
print(df.schema)
print(df.height)
print(df.width)
```

---

# Transform

Gunakan expression native:

```python
df = df.with_columns(
    (pl.col("price") * pl.col("quantity")).alias("total")
)
```

---

# Validation

Contoh:

```python
if df.is_empty():
    raise ValueError(
        "Input data kosong"
    )
```

Cek null:

```python
print(
    df.null_count()
)
```

---

# Logging

Contoh informasi yang berguna:

```bash
pipeline started
input rows
input size
processing time
output rows
output size
errors
```

---

# Output

Untuk dataset besar:

```bash
Parquet
+
partitioning
```

Contoh:

```bash
processed/
├── year=2024/
├── year=2025/
└── year=2026/
```

---

# Error Handling

Gunakan:

```python
try:
    process_data()

except Exception as exc:
    print(
        f"Pipeline failed: {exc}"
    )
    raise
```

Pada production, logging sebaiknya menggunakan `logging` daripada `print`.

---

# Memory Safety

Jangan:

```python
huge_df = query.collect()
```

tanpa mengetahui ukuran hasil.

Gunakan:

```bash
sample
 ↓
estimate
 ↓
decide
 ↓
collect / streaming / sink
```

---

# Production Decision Tree

```bash
Dataset kecil?
    ↓
   YES
    ↓
Eager boleh

Dataset besar?
    ↓
   YES
    ↓
Lazy

Output terlalu besar?
    ↓
   YES
    ↓
Streaming / Sink

Database sangat besar?
    ↓
   YES
    ↓
Batch + Keyset Pagination

Query computationally heavy?
    ↓
   YES
    ↓
Benchmark CPU vs GPU

Dataset sangat besar?
    ↓
   YES
    ↓
Partition + Parquet
```

---

# 12. Prinsip Utama

Jangan memulai optimasi dari GPU.

Mulai dari:

```bash
Data format
    ↓
Query design
    ↓
Lazy
    ↓
Column pruning
    ↓
Predicate pushdown
    ↓
Memory
    ↓
Streaming
    ↓
Partitioning
    ↓
Benchmark
    ↓
GPU
```

Ini membuat pipeline lebih stabil dan lebih mudah dipahami.