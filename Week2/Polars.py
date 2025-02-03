import time
import polars as pl
from datetime import datetime

df = pl.read_parquet("data.parquet")
print(df)

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
df = df.filter(
    pl.col('timestamp').is_between(a,b)
)
color_max = df.select(pl.col('color').value_counts(sort=True))[0,0]
coords = df.group_by('x', 'y').agg(pl.col("__index_level_0__").count().alias("frequency")).sort(pl.col("frequency"), descending=True)
coord = f"{coords[0,0]},{coords[0,1]}"
num_coord = coords[0,2]
color = hex(color_max['color'])
color = color.replace('0x', '#')
num_color = color_max['count']
print("most frequent coordinate: ", coord)
print("coordinate frequency: ", num_coord)
print("most frequent color: ", color)
print("color frequency: ", num_color)
t2 = time.perf_counter()
print("time:", (t2-t1))