import polars as pl


query = (
    pl.scan_parquet(
        "data/input.parquet"
    )
    .select([
        "id",
        "price",
        "quantity",
    ])
)


row_count = (
    query
    .select(pl.len())
    .collect()
    .item()
)


sample_rows = min(
    row_count,
    100_000,
)


sample = (
    query
    .limit(sample_rows)
    .collect()
)


sample_size = (
    sample
    .estimated_size()
)


estimated_size = (
    sample_size
    / sample_rows
    * row_count
)


print(
    f"Rows: {row_count:,}"
)

print(
    f"Sample rows: {sample_rows:,}"
)

print(
    f"Estimated size: "
    f"{estimated_size / 1024**3:.2f} GB"
)