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


result = query.collect(
    engine="gpu"
)

# # Untuk memastikan query tidak diam-diam fallback
# result = query.collect(
#     engine=pl.GPUEngine(
#         raise_on_fail=True
#     )
# )

print(result)