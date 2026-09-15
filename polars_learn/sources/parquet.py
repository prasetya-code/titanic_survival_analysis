import polars as pl


df = pl.DataFrame({
    "id": [1, 2, 3],
    "price": [10000, 20000, 30000],
})


df.write_parquet(
    "data/output.parquet"
)


result = pl.read_parquet(
    "data/output.parquet"
)


print(result)