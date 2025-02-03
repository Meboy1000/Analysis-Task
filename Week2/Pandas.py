from datetime import datetime
import pandas as pd
import time

df = pd.read_parquet("data.parquet")
print(df)
print(df.info())

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
a = pd.Timestamp(a)
b = pd.Timestamp(b)
df = df.query(f'timestamp >= "{a}" and timestamp <= "{b}"')
most_color = df['color'].mode()
num_color = max(df['color'].value_counts())
coords = df.groupby(['x', 'y']).size().reset_index(name='frequency').sort_values(by='frequency', ascending=False).iloc[0]
coord = f"{coords[0]},{coords[1]}"
num_coord = coords[2]
color = hex(most_color[0])
color = color.replace('0x', '#')
print(color)
print(num_color)
print(coord)
print(num_coord)
t2 = time.perf_counter()
print("time:", (t2-t1))