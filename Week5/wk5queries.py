import duckdb as dk
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Please ignore most of this code, I left a lot of bloat semi deliberately, since I wanted my thought process to remain somewhat visible. I also know that a lot of it is unnecesarrily bad






query_1 = """
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    GROUP BY x, y
    ORDER BY x, y
"""
query_10 = """
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE (x % 10) = 0 AND (y % 10) = 0
    GROUP BY x, y
    ORDER BY x, y
"""
query_100 = """
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE (x % 100) = 0 AND (y % 100) = 0
    GROUP BY x, y
    ORDER BY x, y
"""
#results1 = dk.sql(query_1)
#results10 = dk.sql(query_10)
#results100 = dk.sql(query_100)
#print(results1)
#print(results10)
#print(results100)
"""
dk.sql("COPY results1 TO 'results1.csv' (HEADER, DELIMITER ',');")
dk.sql("COPY results10 TO 'results10.csv' (HEADER, DELIMITER ',');")
dk.sql("COPY results100 TO 'results100.csv' (HEADER, DELIMITER ',');")
"""
query_windows = """
    SELECT
    first(color ORDER BY timestamp DESC) as color,
    first(timestamp ORDER BY timestamp DESC) as timestamp,
    x,
    y
    FROM data.parquet
    WHERE timestamp <= '2022-04-04 00:00:00.001'
    GROUP BY x, y
    ORDER by timestamp DESC, x,y
    """
#results2 = dk.sql(query_windows)
#print(results2)
query = """
    SELECT
    MIN(timestamp),
    MAX(timestamp)
    FROM data.parquet
"""
#print(dk.sql(query))
time = datetime.strptime("2022-04-01 13", "%Y-%m-%d %H")
timecap = datetime.strptime("2022-04-05 0", "%Y-%m-%d %H")
avg_01 = []
avg_10 = []
avg_100 = []
avg_a = []
avg_b = []
con = dk.connect(":default:")
while time < timecap:
    next_time = time + timedelta(hours=1)
    q1 = f"""
    WITH R AS(
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE timestamp BETWEEN '{time}' AND '{next_time}'
    GROUP BY x, y
    )
    SELECT AVG(count), '{time}' AS time FROM R
"""
    q2 = f"""
    WITH R AS(
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE (x % 10) = 0 AND (y % 10) = 0 AND timestamp BETWEEN '{time}' AND '{next_time}'
    GROUP BY x, y
    )
    SELECT AVG(count), '{time}' AS time FROM R
"""
    q3 = f"""
    WITH R AS(
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE (x % 100) = 0 AND (y % 100) = 0 AND (x+y) != 0 AND timestamp BETWEEN '{time}' AND '{next_time}'
    GROUP BY x, y
    )
    SELECT AVG(count), '{time}' AS time FROM R
"""
    q4 = f"""
    WITH R AS(
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE (x % 100) = 0 AND timestamp BETWEEN '{time}' AND '{next_time}'
    GROUP BY x, y
    )
    SELECT AVG(count), '{time}' AS time FROM R
"""
    q5 = f"""
    WITH R AS(
    SELECT
    x,
    y,
    COUNT() AS count
    FROM 'data.parquet'
    WHERE (y % 100) = 0 AND timestamp BETWEEN '{time}' AND '{next_time}'
    GROUP BY x, y
    )
    SELECT AVG(count), '{time}' AS time FROM R
"""
    avg_01.append(con.sql(q1))
    avg_10.append(con.sql(q2))
    avg_100.append(con.sql(q3))
    avg_a.append(con.sql(q4))
    avg_b.append(con.sql(q5))
    time = next_time
r1 = avg_01[0]
r2 = avg_10[0]
r3 = avg_100[0]
r4 = avg_a[0]
r5 = avg_b[0]
print('a')
for x in range(1, len(avg_01)-1):
    r1 = r1.union(avg_01[x])
    r2 = r2.union(avg_10[x])
    r3 = r3.union(avg_100[x])
    r4 = r4.union(avg_a[x])
    r5 = r5.union(avg_b[x])
a1 = r1.fetchall()
a2 = r2.fetchall()
a3 = r3.fetchall()
a4 = r4.fetchall()
a5 = r5.fetchall()
x = range(0, len(a1))
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
for element in a1:
    y1.append(element[0])
for element in a2:
    y2.append(element[0])
for element in a3:
    y3.append(element[0])
for element in a4:
    y4.append(element[0])
for element in a5:
    y5.append(element[0])
plt.figure()
plt.bar(x, y1)
plt.ylabel('All Pixels')
plt.savefig('results1.png')
plt.figure()
plt.bar(x,y2)
plt.ylabel('%10 Pixels')
plt.savefig('results2.png')
plt.figure()
plt.bar(x,y3)
plt.ylabel('%100 Pixels')
plt.savefig('results3.png')
plt.figure()
plt.bar(x,y4)
plt.ylabel('%100 Pixels columns')
plt.savefig('results4.png')
plt.figure()
plt.bar(x,y5)
plt.ylabel('%100 Pixels rows')
plt.savefig('results5.png')