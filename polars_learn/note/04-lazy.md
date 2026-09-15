# Apa itu LazyFrame?

LazyFrame adalah representasi query yang belum langsung dieksekusi.

Contoh:

```python
query = (
    pl.scan_parquet("data.parquet")
    .filter(pl.col("age") >= 18)
    .select([
        "id",
        "age",
    ])
)
```

Pada tahap ini data belum sepenuhnya diproses.

---

# collect()

Untuk menjalankan query:

```python
df = query.collect()
```

---

# Mengapa Lazy Penting?

Polars dapat melakukan optimasi seperti:

```bash
Projection Pushdown
Predicate Pushdown
Common Subplan Elimination
Expression Simplification
Join Optimization
```

Contoh:

```python
query = (
    pl.scan_parquet("data.parquet")
    .filter(pl.col("age") >= 18)
    .select([
        "id",
        "age",
    ])
)
```

Polars dapat mengetahui bahwa hanya `id` dan `age` yang diperlukan.

---

# explain()

Untuk melihat query plan:

```python
print(query.explain())
```

Gunakan ini ketika ingin memahami bagaimana Polars menjalankan query.

---

# Jangan collect terlalu awal

Kurang ideal:

```python
df = query.collect()

df = df.filter(...)
df = df.with_columns(...)
```

Lebih baik:

```python
query = (
    query
    .filter(...)
    .with_columns(...)
)

df = query.collect()
```

---

# Collect Sekali

Ideal:

```python
query = (
    pl.scan_parquet("data.parquet")
    .filter(...)
    .with_columns(...)
    .group_by(...)
    .agg(...)
)

result = query.collect()
```

---

# Lazy sebagai Default untuk Dataset Besar

Gunakan:

```python
scan_*
```

kemudian:

```python
query
    ↓
optimization
    ↓
collect
```

Ini menjadi pola utama ketika bekerja dengan dataset besar.