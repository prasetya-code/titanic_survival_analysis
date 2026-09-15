import time
import polars as pl


query = (
    pl.scan_parquet(
        "data/input.parquet"
    )
    .filter(
        pl.col("age") >= 18
    )
    .with_columns(
        (
            pl.col("price")
            * pl.col("quantity")
        ).alias("total")
    )
)


# CPU
start = time.perf_counter()

cpu_result = query.collect(
    engine="in-memory"
)

cpu_time = (
    time.perf_counter()
    - start
)


# GPU
start = time.perf_counter()

gpu_result = query.collect(
    engine="gpu"
)

gpu_time = (
    time.perf_counter()
    - start
)


print(
    f"CPU : {cpu_time:.2f}s"
)

print(
    f"GPU : {gpu_time:.2f}s"
)

print(
    f"Speedup: "
    f"{cpu_time / gpu_time:.2f}x"
)