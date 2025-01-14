import sqlite3
import csv

with open ('2022_place_canvas_history.csv', 'r') as f:
    connection = sqlite3.connect("data.db")
    reader = csv.reader(f)
    columns = next(reader) 
    print(columns)
    query = 'INSERT INTO Place({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    init = "CREATE TABLE Place(timestamp, user_id, pixel_color, coordinate)"
    cursor = connection.cursor()
    for data in reader:
        cursor.execute(query, data)
    connection.commit()