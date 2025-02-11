import duckdb as dk


query_1 = """
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'wk3data.parquet'
    GROUP BY x, y
    ORDER BY x, y
"""
query_10 = """
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'wk3data.parquet'
    where (x % 10) = 0 AND (y % 10) = 0
    GROUP BY x, y
    ORDER BY x, y
"""
query_100 = """
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'wk3data.parquet'
    where (x % 100) = 0 AND (y % 100) = 0
    GROUP BY x, y
    ORDER BY x, y
"""
results1 = dk.sql(query_1)
results10 = dk.sql(query_10)
results100 = dk.sql(query_100)
print(results1)
print(results10)
print(results100)
dk.sql("COPY results1 TO 'results1.csv' (HEADER, DELIMITER ',');")
dk.sql("COPY results10 TO 'results10.csv' (HEADER, DELIMITER ',');")
dk.sql("COPY results100 TO 'results100.csv' (HEADER, DELIMITER ',');")