# Apa itu Parquet?

Parquet adalah format penyimpanan data columnar. Berbeda dengan CSV yang berbasis bash. Parquet dirancang untuk workload analitik.

---

# Mengapa Parquet?

Keuntungan:

* columnar storage
* compression
* schema
* column pruning
* predicate pushdown
* cocok untuk Lazy API
* cocok untuk dataset besar

---

# Membaca Parquet

```python
df = pl.read_parquet(
    "data.parquet"
)
```

Lazy:

```python
query = pl.scan_parquet(
    "data.parquet"
)
```

---

# Menulis Parquet

```python
df.write_parquet(
    "output.parquet"
)
```

---

# Lazy Output

Untuk output besar:

```python
(
    query
    .sink_parquet(
        "output.parquet"
    )
)
```

---

# Column Pruning

Misalnya dataset memiliki:

```bash
id
name
email
age
country
price
quantity
created_at
```

Tetapi hanya membutuhkan:

```bash
id
price
quantity
```

Gunakan:

```python
query = (
    pl.scan_parquet("data.parquet")
    .select([
        "id",
        "price",
        "quantity",
    ])
)
```

---

# Predicate Pushdown

Contoh:

```python
query = (
    pl.scan_parquet("data.parquet")
    .filter(
        pl.col("price") > 100000
    )
)
```

Polars dapat mendorong filter sedekat mungkin dengan sumber data.

---

# Partitioned Parquet

Untuk dataset sangat besar:

```bash
data/
├── year=2024/
├── year=2025/
└── year=2026/
```

Atau:

```bash
data/
├── year=2026/
│   ├── month=01/
│   ├── month=02/
│   └── month=03/
```

Partition sebaiknya mengikuti pola query yang sering digunakan, misal:

```py
# Tulis ke Parquet dengan partisi menggunakan PyArrow
df.write_parquet(
    "output_dataset", 
    use_pyarrow=True,
    pyarrow_options={"partition_cols": ["tahun", "bulan"]}
)
```

maka hasilnya akan:

```bash
output_dataset/
├── tahun=2025/
│   └── bulan=12/
│       └── data.parquet
└── tahun=2026/
    ├── bulan=1/
    │   └── data.parquet
    └── bulan=2/
        └── data.parquet
```

---

# Rule

Untuk workload analitik:

```bash
CSV
 ↓
Parquet
 ↓
Lazy
 ↓
Filter + Select
 ↓
Process
```

Biasanya jauh lebih baik daripada:

```bash
CSV
 ↓
full DataFrame
 ↓
process
```