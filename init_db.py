import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO highlights (content) VALUES (?)",
            ('test highlight 1',)
            )

cur.execute("INSERT INTO highlights (content) VALUES (?)",
            ('test highlight 2',)
            )

connection.commit()
connection.close()