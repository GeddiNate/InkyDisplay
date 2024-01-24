import sqlite3
import csv

note_sep = '=========='

def from_my_clippings_(cur, filename):
    with open(filename, encoding='utf-8-sig') as file:
        items = file.read().split(note_sep)
        data = [item.split('\n') for item in items if item != '']
        print(data)

def from_emailed_csv(cur, filename):
    with open(filename, encoding='utf-8') as file:
        reader = list(csv.reader(file))

        title, subtitle = reader[1][0].split(':')
        title.strip().title()
        subtitle.strip().title()

        author = reader[2][0][2:].strip()

        cur.execute("INSERT INTO books (title, subtitle) VALUES (?,?)",
            (title.strip().title(), subtitle.strip().title())
            )
        book_id = cur.lastrowid
        
        cur.execute("INSERT INTO authors (name) VALUES (?)",
            (author,)
            )
        author_id = cur.lastrowid

        cur.execute("INSERT INTO book_authors (book_id, author_id) VALUES (?,?)",
            (book_id, author_id)
            )

        for row in reader[8:]:
            content_type = row[0].split(' ')[0]
            location = int(row[1].split(' ')[1])
            content = row[3]
            if content_type == 'Highlight':
                cur.execute("INSERT INTO highlights (content, location, book_id) VALUES (?,?,?)",
                    (content, location, book_id)
                    )
            elif content_type == 'Note':
                fetched_row = cur.execute('SELECT highlight_id FROM highlights WHERE book_id=? AND location=?',
                (book_id, location)
                ).fetchall()
                #print(fetched_row[0]['highlight_id'])
                if fetched_row:
                    cur.execute('UPDATE highlights SET note=? WHERE highlight_id=?',
                    (content, fetched_row[0]['highlight_id'])
                    )

    
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

conn = get_db_connection() 
cur = conn.cursor()
#from_kindle_clippings_file('tmp', 'My Clippings.txt')
from_emailed_csv(cur, 'Oathbringer_ Book Three of the Stormlight Archive-Notebook.csv')

conn.commit()
conn.close()