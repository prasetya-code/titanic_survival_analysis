# File Size ≠ RAM Usage

Jangan menganggap:

```bash
data.parquet = 2 GB
```

berarti:

```bash
DataFrame = 2 GB RAM
```

Parquet dapat menggunakan compression.

Ketika dibaca ke memory, data dapat menjadi jauh lebih besar.

---

# Rule of Thumb

Sebagai panduan awal:

```bash
< 500 MB
    eager(dataframe) biasanya aman

500 MB – 2 GB
    biasanya masih nyaman

2 – 5 GB
    perhatikan RAM

5 – 10 GB
    pertimbangkan streaming

10 – 50 GB
    hindari full collect

50 – 100 GB
    streaming / batch / sink

> 100 GB
    partition + streaming + sink
```

Ini bukan batas resmi Polars.

Hasil sebenarnya tergantung RAM, schema, operasi, dan data.

---

# estimated_size() - hanya bisa digunakan jika data sudah dalam bentuk dataframe ≠ lazy frame

Untuk DataFrame yang sudah ada:

```python
size = df.estimated_size()

print(
    f"{size / 1024**3:.2f} GB"
)
```

---

# Masalahnya

Jangan melakukan:

```python
df = huge_query.collect()
```

hanya untuk mengetahui apakah hasilnya terlalu besar.

Jika hasil sebenarnya 100 GB, Anda sudah terlanjur mencoba membuat DataFrame 100 GB.

---

# Estimasi dengan Sample

Pertama hitung jumlah baris:

```python
row_count = (
    query
    .select(pl.len())
    .collect()
    .item()
)
```

Kemudian ambil sample:

```python
sample_rows = min(
    row_count,
    100_000,
)

sample = (
    query
    .limit(sample_rows)
    .collect()
)
```

Hitung:

```python
sample_size = (
    sample.estimated_size()
)
```

Estimasi:

```python
estimated_size = (
    sample_size
    / sample_rows
    * row_count
)
```

---

# Safety Factor

Estimasi sample tidak selalu akurat.

Misalnya:

```python
estimated_size = 8 * 1024**3
```

Gunakan safety factor:

```python
safe_size = (
    estimated_size * 1.5
)
```

---

# Multiple Samples

Jika data sangat bervariasi:

```python
sample_1 = (
    query
    .head(100_000)
    .collect()
)

sample_2 = (
    query
    .slice(5_000_000, 100_000)
    .collect()
)

sample_3 = (
    query
    .tail(100_000)
    .collect()
)
```

Bandingkan ukuran ketiga sample.

---

# estimated_size Bukan Peak RAM

`estimated_size()` menunjukkan estimasi ukuran DataFrame.

Peak RAM dapat lebih besar karena:

```bash
DataFrame
+
intermediate data
+
join
+
sort
+
group_by
+
buffers
+
Python
+
OS
```

Karena itu selalu sisakan headroom.