import pandas as pd
import time

def color_int(color: str):
    num = int(color.replace("#", ""), 16)
    return num

def fixer(arg):
    nums = arg.string.split(',')
    coord = f'{nums[0]},{nums[1]}'
    return coord


t1 = time.perf_counter()
with pd.read_csv("./2022_place_canvas_history.csv", usecols=['timestamp','pixel_color','coordinate'], skip_blank_lines=True, chunksize=1000000) as reader:

    chunks = []
    for chunk in reader:
        t2 = time.perf_counter()
        print("time:", t2-t1)
        t1 = time.perf_counter()
        chunk['timestamp'] = chunk['timestamp'].str.replace('\.\d{1,3}', '', regex=True)
        chunk['timestamp'] = chunk['timestamp'].str.replace(' UTC', '', regex=False)
        chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce") #not future proof, ignoring errors is deprecated
        chunk['color'] = pd.to_numeric(chunk['pixel_color'].transform(color_int), downcast='unsigned')
        chunk.drop(['pixel_color'], axis=1, inplace=True)
        chunk['coordinate'] = chunk['coordinate'].str.replace("\w{1,4},\w{1,4},.*", fixer, regex=True)
        chunk[['x','y']] = chunk['coordinate'].str.split(',', expand=True)
        chunk['x'] = pd.to_numeric(chunk['x'], downcast='unsigned')
        chunk['y'] = pd.to_numeric(chunk['y'], downcast='unsigned')
        chunk.drop(['coordinate'], axis=1, inplace=True)
        print(chunk)
        print(chunk.info())
        chunks.append(chunk)
        t2 = time.perf_counter()
        print("time:", t2-t1)
    final_df = pd.concat(chunks, ignore_index=True)
    final_df = final_df.sort_values(by=['timestamp'])
    print(final_df.info())
    final_df.to_parquet('data.parquet', compression='snappy', engine='auto')
