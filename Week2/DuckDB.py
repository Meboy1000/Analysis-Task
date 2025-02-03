import duckdb as dk
from datetime import datetime
import time
in1 = input("Enter first timestamp:")
in2 = input("Enter second timestamp:")
a = datetime.strptime(in1, "%Y-%m-%d %H")
b = datetime.strptime(in2, "%Y-%m-%d %H")
print(a, b)
while a > b:
    print("Invalid Dates")
    in1 = input("Enter first timestamp:")
    in2 = input("Enter second timestamp:")
    a = datetime.strptime(in1, "%Y-%m-%d %H")
    b = datetime.strptime(in2, "%Y-%m-%d %H")
t1 = time.perf_counter()
query = f"""WITH R AS(
    SELECT color, count(color) AS pnum FROM 'data.parquet'
    WHERE timestamp BETWEEN '{a}' AND '{b}'
    GROUP BY color
    ORDER BY pnum DESC
    LIMIT 1
    ),
    K AS(
    SELECT x, y, count(*) AS cnum FROM 'data.parquet'
    WHERE timestamp BETWEEN '{a}' AND '{b}'
    GROUP BY x, y
    ORDER BY cnum DESC
    LIMIT 1
    )

    SELECT color, pnum, x, y, cnum FROM R, K
    """


results = dk.sql(query)
print(results)
t2 = time.perf_counter()
print("time:", t2-t1)