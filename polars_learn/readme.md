# Dir Structure

```bash
polars-learn/
│
├── 00-roadmap.md 
├── 01-dasar-polars.md 
├── 02-read-data.md 
├── 03-expression.md 
├── 04-lazy.md 
├── 05-parquet.md 
├── 06-memory.md 
├── 07-streaming.md 
├── 08-database.md 
├── 09-gpu.md 
├── 10-benchmarking.md 
├── 11-production.md
│
└── Sources/ 
    ├── basic.py 
    ├── lazy.py 
    ├── parquet.py 
    ├── memory.py 
    ├── streaming.py 
    ├── database.py 
    ├── gpu.py 
    └── benchmark.py
```

---

# Level Pembelajaran

## Level 1 — Fundamental

File:
1. 01-dasar-polars.md
2. 02-read-data.md
3. 03-expression.md
4. 04-lazy.md

Fokus:
- DataFrame
- Series
- Expression
- filter
- select
- with_columns
- group_by
- LazyFrame


## Level 2 — Large Dataset

File:
1. 05-parquet.md
2. 06-memory.md
3. 07-streaming.md

Fokus:
- Parquet
- memory
- query optimization
- streaming
- sink


## Level 3 — Data Engineering

File:
1. 08-database.md

Fokus:
- database
- batch processing
- keyset pagination
- database → Polars → Parquet


## Level 4 — Performance

File:
1. 09-gpu.md
2. 10-benchmarking.md

Fokus:
- GPU
- CPU vs GPU
- benchmarking
- profiling


## Level 5 — Production

File:
1. 11-production.md

Fokus:
- pipeline
- partitioning
- logging
- monitoring
- error handling
- reproducibility

---

# NOTE

1. pada markdown memory, pastikan sudah include semua column dan untuk akurat bisa menggunakan persentase dari total length nya, misal:
    ```python
    # 1. Tentukan persentase sampel (contoh: 10% = 0.10)
    sample_percentage = 0.10  

    # 2. Hitung total baris
    row_count = (
        query
        .select(pl.len())
        .collect()
        .item()
    )

    # 3. Hitung jumlah baris sampel berdasarkan persentase
    # Menggunakan int() dan max(..., 1) agar minimal mengambil 1 baris jika data tidak kosong
    sample_rows = min(
        row_count,
        max(1 if row_count > 0 else 0, int(row_count * sample_percentage))
    )

    # 4. Ambil sampel (mengambil n baris pertama)
    sample = (
        query
        .limit(sample_rows)
        .collect()
    )
    ```