import sqlite3
import time
from datetime import datetime
with sqlite3.connect("data.db") as con:
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
    SELECT pixel_color, count(pixel_color) AS pnum FROM Place
    WHERE timestamp BETWEEN '{a}' AND '{b}'
    GROUP BY pixel_color
    ORDER BY pnum DESC
    LIMIT 1
    ),
    K AS(
    SELECT coordinate, count(*) AS cnum FROM Place
    WHERE timestamp BETWEEN '{a}' AND '{b}'
    GROUP BY coordinate
    ORDER BY cnum DESC
    LIMIT 1
    )

    SELECT pixel_color, coordinate, pnum, cnum FROM R, K
    """
    cursor = con.cursor()
    thing = cursor.execute(query)
    print(query)
    print(cursor)
    print("bees", thing)
    for row in thing:
        print("row", row)
    t2 = time.perf_counter()
    print("time:", t2-t1)