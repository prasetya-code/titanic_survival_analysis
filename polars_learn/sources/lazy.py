import polars as pl


query = (
    pl.scan_parquet(
        "data/input.parquet"
    )
    .filter(
        pl.col("age") >= 18
    )
    .select([
        "id",
        "age",
        "price",
    ])
    .with_columns(
        (
            pl.col("price") * 2
        ).alias("price_double")
    )
)


print("=== QUERY PLAN ===")
print(query.explain())


result = query.collect()


print("=== RESULT ===")
print(result)