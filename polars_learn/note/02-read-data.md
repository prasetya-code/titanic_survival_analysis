# CSV

Untuk dataset kecil:

```python
import polars as pl

df = pl.read_csv("data.csv")
```

---

# CSV dengan Schema

```python
df = pl.read_csv(
    "data.csv",
    schema_overrides={
        "id": pl.Int64,
        "price": pl.Float64,
    },
)
```

---

# Parquet

```python
df = pl.read_parquet("data.parquet")
```

---

# Lazy CSV

Jika ingin menggunakan Lazy API:

```python
query = pl.scan_csv("data.csv")
```

Kemudian:

```python
df = query.collect()
```

---

# Lazy Parquet

```python
query = pl.scan_parquet("data.parquet")
```

Ini sangat penting untuk dataset besar.

---

# Memilih Kolom

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

# Filter Saat Membaca

```python
query = (
    pl.scan_parquet("data.parquet")
    .filter(
        pl.col("price") > 10000
    )
)
```

---

# Mengapa `scan_*`?

Perbedaan:

```python
pl.read_parquet()
```

langsung membaca data menjadi DataFrame.

Sedangkan:

```python
pl.scan_parquet()
```

membuat LazyFrame.

LazyFrame memungkinkan Polars mengoptimalkan query sebelum data diproses.

---

# Eager vs Lazy

Eager:

```bash
read
 ↓
DataFrame
 ↓
filter
 ↓
result
```

Lazy:

```bash
scan
 ↓
LazyFrame
 ↓
query
 ↓
optimization
 ↓
collect
 ↓
result
```

---

# Kapan Menggunakan?

Dataset kecil:

```python
pl.read_csv(...)
```

Dataset besar:

```python
pl.scan_parquet(...)
```

Sebisa mungkin gunakan Parquet untuk workload analitik besar.