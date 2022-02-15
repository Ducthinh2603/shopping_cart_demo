import sqlite3

DB_PATH = './models/my_data.db'

with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM Cart_item")
    data =c.fetchall()
    for each in data:
        print(each)