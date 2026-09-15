import polars as pl


BATCH_SIZE = 1_000_000

last_id = 0


while True:

    query_sql = f"""
        SELECT
            id,
            user_id,
            quantity,
            price,
            created_at
        FROM transactions
        WHERE id > {last_id}
        ORDER BY id
        LIMIT {BATCH_SIZE}
    """

    df = pl.read_database(
        query=query_sql,
        # connection harus disesuaikan dengan database/driver yang Anda gunakan
        connection=connection,
    )

    if df.is_empty():
        break

    df = df.with_columns(
        (
            pl.col("quantity")
            * pl.col("price")
        ).alias("total")
    )

    output_path = (
        f"data/output/"
        f"batch_{last_id}.parquet"
    )

    df.write_parquet(
        output_path
    )

    last_id = (
        df["id"].max()
    )

    print(
        f"Processed until id={last_id}"
    )