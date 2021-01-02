import sqlite3

connection = sqlite3.connect('database.sqlite')
cur = connection.cursor()
cur.execute("""CREATE TABLE student
                (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                name VARCHAR (32));
            """)
cur.close()
connection.close()