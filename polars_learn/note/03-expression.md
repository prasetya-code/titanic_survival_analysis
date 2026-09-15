# Apa itu Expression?

Expression adalah salah satu konsep paling penting dalam Polars.

Contoh:

```python
pl.col("price")
```

Expression dapat digunakan untuk:

* mengambil kolom
* transformasi
* filter
* agregasi
* membuat kolom baru

---

# Mengambil Kolom

```python
pl.col("price")
```

---

# Operasi Matematika

```python
pl.col("price") * pl.col("quantity")
```

---

# Alias - menambah atau mengubah kolom (jika nama kolom sudah ada)

```python
(
    pl.col("price") * pl.col("quantity")
).alias("total")
```

---

# with_columns(cara implementasi expression)

```python
df = df.with_columns(
    (
        pl.col("price") * pl.col("quantity")
    ).alias("total")
)
```

---

# Multiple Expressions(multi expression dengan array)

```python
df = df.with_columns([
    (
        pl.col("price") * pl.col("quantity")
    ).alias("total"),

    (
        pl.col("price") * 2
    ).alias("price_double"),
])
```

---

# Filter

```python
df.filter(
    pl.col("age") >= 18
)
```

Multiple kondisi:

```python
df.filter(
    (pl.col("age") >= 18)
    & (pl.col("country") == "ID")
)
```

---

# Conditional

```python
df.with_columns(
    pl.when(pl.col("age") >= 18)
      .then(pl.lit("adult"))
      .otherwise(pl.lit("minor"))
      .alias("category")
)
```

---

# String

```python
df.with_columns(
    pl.col("name").str.to_lowercase()
)
```

---

# Numeric

```python
df.with_columns(
    pl.col("price").round(2)
)
```

---

# Aggregation

```python
df.select(
    pl.col("price").mean()
)
```

Contoh:

```python
df.select([
    pl.col("price").min(),
    pl.col("price").max(),
    pl.col("price").mean(),
])
```

---

# Hindari Python Loop

Kurang ideal:

```python
for value in values:
    ...
```

Lebih baik gunakan expression Polars:

```python
pl.col("price") * pl.col("quantity")
```

Native expression memungkinkan Polars melakukan optimasi dengan lebih baik.