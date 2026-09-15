# Apa itu Polars?

Polars adalah library DataFrame untuk Python yang dirancang untuk pemrosesan data yang cepat dan efisien. Konsep dasarnya mirip dengan pandas:

```python
DataFrame
Series
filter
select
group_by
join
sort
```

Namun Polars memiliki sistem expression dan Lazy API yang sangat penting untuk dataset besar.

---

# Instalasi

```bash
pip install polars
```

Cek instalasi:

```python
import polars as pl

print(pl.__version__)
```

---

# DataFrame

DataFrame adalah tabel data.

Contoh:

```python
import polars as pl

df = pl.DataFrame({
    "name": ["Andi", "Budi", "Citra"],
    "age": [25, 30, 22],
})

print(df)
```

Struktur:

```bash
name    age
Andi    25
Budi    30
Citra   22
```

---

# Melihat Data

```python
print(df)
```

Melihat schema:

```python
print(df.schema)
```

Melihat nama kolom:

```python
print(df.columns)
```

Melihat jumlah baris:

```python
print(df.height)
```

Melihat jumlah kolom:

```python
print(df.width)
```

---

# Series

Series adalah satu kolom.

```python
ages = df["age"]

print(ages)
```

---

# Select

Mengambil kolom:

```python
df.select("name")
```

Beberapa kolom:

```python
df.select([
    "name",
    "age",
])
```

---

# Filter

```python
df.filter(
    pl.col("age") >= 25
)
```

---

# Menambah Kolom

```python
df.with_columns(
    (pl.col("age") + 1).alias("age_next_year")
)
```

---

# Sorting

```python
df.sort("age")
```

Descending:

```python
df.sort(
    "age",
    descending=True,
)
```

---

# Group By

```python
df.group_by("age").agg(
    pl.len().alias("count")
)
```

---

# Prinsip Dasar

Biasakan membaca:

```python
pl.col("nama_kolom")
```

sebagai:

> "Expression yang merepresentasikan kolom tersebut."

Contoh:

```python
pl.col("price") * pl.col("quantity")
```

berarti:

```text
price × quantity
```