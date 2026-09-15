import polars as pl


df = pl.DataFrame({
    "product": ["A", "B", "C"],
    "price": [10000, 20000, 15000],
    "quantity": [2, 3, 4],
})


print("=== DATA ===")
print(df)


df = df.with_columns(
    (
        pl.col("price")
        * pl.col("quantity")
    ).alias("total")
)


print("=== WITH TOTAL ===")
print(df)


result = (
    df
    .filter(pl.col("total") > 30000)
    .sort("total", descending=True)
)


print("=== RESULT ===")
print(result)