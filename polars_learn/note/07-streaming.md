# Apa itu Streaming?

Streaming memungkinkan query besar diproses secara bertahap sehingga tekanan memory dapat dikurangi.

Contoh:

```python
result = query.collect(
    engine="streaming"
)
```

---

# Kapan Streaming?

Gunakan ketika:

```bash
dataset besar
+
query cukup berat
+
full collect terlalu besar
```

---

# Streaming Tidak Berarti Tanpa Memory

Misalnya hasil akhir tetap:

```bash
30 GB
```

Jika menggunakan:

```python
query.collect(
    engine="streaming"
)
```

hasil akhirnya tetap harus menjadi DataFrame jika Anda meminta `collect()`.

Jadi streaming bukan berarti:

> "30 GB DataFrame menjadi tidak membutuhkan RAM."

---

# Sink

Jika tidak perlu menyimpan seluruh hasil sebagai DataFrame:

```python
(
    query
    .sink_parquet(
        "output.parquet"
    )
)
```

Ini lebih cocok untuk output yang sangat besar.

---

# Pipeline

Pola umum:

```bash
Input
 ↓
Lazy Query
 ↓
Filter
 ↓
Select
 ↓
Transform
 ↓
Streaming
 ↓
Parquet
```

---

# Contoh

```python
query = (
    pl.scan_parquet(
        "data/input.parquet"
    )
    .filter(
        pl.col("age") >= 18
    )
    .with_columns(
        (pl.col("price") * pl.col("quantity")).alias("total")
    )
)

query.collect(
    engine="streaming"
)
```

---

# Streaming vs Sink

Gunakan:

```python
collect(engine="streaming")
```

jika:

```bash
hasil akhir masih perlu dipakai sebagai DataFrame
```

Gunakan:

```python
sink_parquet()
```

jika:

```bash
hasil sangat besar dan langsung ingin disimpan
```

---

# Konsep Penting

```bash
Streaming
    ↓
mengurangi memory pressure

Sink
    ↓
menghindari materialisasi seluruh hasil
```

Keduanya bukan pengganti partitioning.