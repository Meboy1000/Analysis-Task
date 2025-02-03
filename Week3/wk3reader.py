import time
import duckdb as dk
from datetime import datetime
import webcolors as wc

color_dict = {}
def color_ranker(color_list):
    output = {}
    for row in color_list:
        name = color_namer(row[0])
        output[name] = row[1]
    return output

def color_namer(number: int):
    col_hex = '#%06X' % number
    try:
        # Get the color name directly
        return wc.hex_to_name(col_hex)
    except ValueError:
        # If exact match not found, find the closest color
        return closest_color(wc.hex_to_rgb(col_hex))

def closest_color(requested_color):
    min_colors = {}
    for key, code in color_dict.items():
        r_c, g_c, b_c = wc.hex_to_rgb(code)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = key
    return min_colors[min(min_colors.keys())]
#init for color names.
for name in wc.names():
    color_dict[name] = wc.name_to_hex(name)
# 2022-04-04 00 <- test input format
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
query = f"""
    WITH F AS(
    WITH J AS(
    WITH K AS(
    WITH R AS(
        SELECT 
        user_id,
        timestamp,
        LEAD(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) AS next_timestamp,
        LAG(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) AS last_timestamp
        FROM 'wk3data.parquet'
        WHERE timestamp BETWEEN '{a}' AND '{b}'
    )

    SELECT user_id, timestamp, next_timestamp, last_timestamp,
    EXTRACT(EPOCH FROM next_timestamp - timestamp) AS next_timediff,
    EXTRACT(EPOCH FROM timestamp - last_timestamp) AS last_timediff,
    CASE
        WHEN next_timediff >= 900 OR next_timestamp IS NULL THEN 'END'
        WHEN last_timediff >= 900 OR last_timestamp IS NULL THEN 'START'
        ELSE 'MID'
    END AS flag
    FROM R
    WHERE next_timediff < 900 OR last_timediff < 900
    )
    SELECT 
    user_id,
    timestamp,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as row,
    flag
    FROM K
    WHERE flag IN ('END', 'START')
    ORDER BY user_id, timestamp
    )
    SELECT 
    user_id,
    timestamp,
    NTH_VALUE(timestamp, row-1) OVER (PARTITION BY user_id ORDER BY timestamp) as last_timestamp,
    EXTRACT(EPOCH FROM timestamp - last_timestamp) AS timediff,
    row,
    flag
    FROM J
    ORDER BY user_id, timestamp
    )
    SELECT AVG(timediff)/60 AS avg_session
    FROM F
    WHERE flag = 'END'
    """
query_2 = """
UPDATE sessions_1
SET next_timestamp = nextest
WHERE next_timestamp = nexter
"""
query_colors = f"""
    WITH R AS(
        SELECT DISTINCT
        color,
        user_id 
        FROM 'wk3data.parquet'
        WHERE timestamp BETWEEN '{a}' AND '{b}'
    )
    SELECT color,
     COUNT(user_id) AS users
     FROM R
     GROUP BY color
     ORDER BY users DESC
"""
query_firsts = f"""
    WITH R AS(
    SELECT
    user_id,
    MIN(timestamp) as timestamp
    FROM 'wk3data.parquet'
    GROUP BY user_id
    )
    SELECT
    COUNT(user_id)
    FROM R
    WHERE timestamp BETWEEN '{a}' AND '{b}'
"""
query_percentiles = f"""
WITH R AS (
    SELECT
    user_id,
    COUNT(timestamp) as count
    FROM 'wk3data.parquet'
    WHERE timestamp BETWEEN '{a}' AND '{b}'
    GROUP BY user_id
)
SELECT
PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY count) AS Fifty,
PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY count) AS Seventy_Five,
PERCENTILE_DISC(0.9) WITHIN GROUP (ORDER BY count) AS Ninety,
PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY count) AS Ninety_Nine
FROM R
"""
sessions_1 = dk.sql(query)
print(sessions_1)
colors = dk.sql(query_colors).fetchall()
rankings = color_ranker(colors)
rank = 1
for key, value in rankings.items():
    print(f"{rank}. {key}, {value}")
    rank += 1
new_users = dk.sql(query_firsts)
print(new_users)
percentiles = dk.sql(query_percentiles)
print(percentiles)
t2 = time.perf_counter()
print("time:", t2-t1)