# Mengapa Benchmark?

Jangan menentukan:

```bash
GPU lebih cepat
```

atau:

```bash
CPU lebih cepat
```

hanya berdasarkan asumsi.

Ukur secara langsung.

---

# Gunakan Dataset yang Sama

Benchmark harus menggunakan:

```bash
dataset sama
query sama
schema sama
output sama
```

---

# Benchmark CPU

```python
import time

start = time.perf_counter()

result = query.collect(
    engine="in-memory"
)

cpu_time = (
    time.perf_counter()
    - start
)

print(
    f"CPU: {cpu_time:.2f}s"
)
```

---

# Benchmark GPU

```python
start = time.perf_counter()

result = query.collect(
    engine="gpu"
)

gpu_time = (
    time.perf_counter()
    - start
)

print(
    f"GPU: {gpu_time:.2f}s"
)
```

---

# Hitung Speedup

```python
speedup = (
    cpu_time / gpu_time
)

print(
    f"Speedup: {speedup:.2f}x"
)
```

Misalnya:

```bash
CPU = 100 seconds
GPU = 25 seconds
```

maka:

```bash
100 / 25 = 4x
```

---

# Jangan Hanya Mengukur Waktu

Perhatikan:

```bash
execution time
RAM
VRAM
CPU utilization
GPU utilization
I/O
output size
```

---

# Warm-up

Untuk benchmark yang lebih konsisten, jalankan query terlebih dahulu sebelum pengukuran utama. Tujuannya untuk mengurangi pengaruh initialization overhead.

---

# Benchmark Beberapa Kali

Contoh:

```bash
run 1
run 2
run 3
run 4
run 5
```

Kemudian gunakan:

```bash
median
```

atau statistik yang sesuai.

---

# Benchmark yang Baik

Contoh:

```bash
Dataset:
100 GB

Query:
filter + group_by + aggregation

CPU:
125 sec

GPU:
42 sec

Speedup:
2.98x
```

Ini lebih berguna daripada hanya mengatakan:

> GPU lebih cepat.

---

# Kesimpulan

Benchmark digunakan untuk mengambil keputusan berdasarkan data:

```bash
CPU
vs
GPU
vs
Hybrid
```

bukan berdasarkan asumsi.