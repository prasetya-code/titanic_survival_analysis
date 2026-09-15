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

# # Untuk output yang sangat besar
# query.sink_parquet("data/output.parquet")

result = query.collect(
    engine="streaming"
)


print(result)