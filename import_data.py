import sqlite3
import csv
import os
import re

note_sep = '=========='
test_dir_path = 'csv'

TITLE_LINE = 1
AUTHOR_LINE = 2
FIRST_DATA_ROW = 8
TYPE_COLUMN = 0
LOCATION_COLUMN = 1
CONTENT_COLUMN = 3



def from_my_clippings_(cur, filename):
    with open(filename, encoding='utf-8-sig') as file:
        items = file.read().split(note_sep)
        data = [item.split('\n') for item in items if item != '']
        print(data)

def from_emailed_csv(cur, filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))

        # Get title and subtitle from the csv file.
        tmp = re.split(r'[:\(]', reader[TITLE_LINE][TYPE_COLUMN])
        title = tmp[0].strip().title()
        subtitle = tmp[1].strip().title()

        if ')' in subtitle: # Remove closeing parenthetical from the subtitle.
            subtitle = subtitle[:-1]

        # Get the author(s) and remove the leading "by".
        authors_text = reader[AUTHOR_LINE][TYPE_COLUMN][2:].strip()
        if ',' in authors_text: # if multiple authors sperated by comma
            authors = [item.strip() for item in authors_text.split(',')]
        else: # Put the author in a single element array so there is only one itteration.
            authors = [authors_text]  
        
        author_ids = []
        for author in authors:
            try: # Insert author into the DB.
                cur.execute("INSERT INTO authors (name) VALUES (?)",
                    (author,)
                    )
                author_ids.append(cur.lastrowid) # Save the author_id for later.
            except sqlite3.IntegrityError as e: # If it is already in the DB get the author_id.
                cur.execute("SELECT author_id FROM authors WHERE name=?",
                    (author,)
                    )
                author_ids.append(cur.fetchone()[0]) # Save the author_id for later.

        try: # Insert book if it is not in the DB.
            cur.execute("INSERT INTO books (title, subtitle) VALUES (?,?)",
                (title, subtitle)
                )
            book_id = cur.lastrowid # Save the book_id for later.
        except sqlite3.IntegrityError as e: # If it is in the DB get the book_id.
            cur.execute("SELECT book_id FROM books WHERE title=? AND subtitle=?",
                (title, subtitle)
                )
            book_id = cur.fetchone()[0] # Save the book_id for later.
        else: # if a new book is inserted link it to each author.
            for author_id in author_ids: 
                cur.execute("INSERT INTO book_authors (book_id, author_id) VALUES (?,?)",
                (book_id, author_id)
                )

        highlight_rows = reader[FIRST_DATA_ROW:]
        last_highlight_id = None
        for i in range(len(highlight_rows)): # For each highlight or note
            row = highlight_rows[i]

            content_type = row[TYPE_COLUMN]
            loc_type, location = row[LOCATION_COLUMN].split(' ') # loc_type is the page or location. Location contains the number.
            
            # Clean data so it matches the field names in the DB.
            if loc_type == "Location": 
                loc_type = 'location_start'
            else: # The page field in DB is lowerae
                loc_type = loc_type.lower()

            content = row[CONTENT_COLUMN] # Get the highlighted text or the note.
            if 'Highlight' in content_type:
                try : # Insert Highlight if it is not in the DB.
                    content_type, color = content_type.split(' ')
                    cur.execute(f"INSERT INTO highlights (content, color, {loc_type}, book_id) VALUES (?,?,?,?)",
                        (content, color, location, book_id)
                        ) 
                    last_highlight_id = cur.lastrowid
                except sqlite3.IntegrityError as e:
                    print(f'Insert failed due to unique constraint: {e}')
            elif 'Note' in content_type:
                """ All my notes are on highlighted passages and there is only one note per passages
                    so this works for me. In the future I should find a better solution than this but
                    I'm going to move on to other aspects of this project for now."""
                cur.execute(f"INSERT INTO notes (note, {loc_type}, highlight_id, book_id) VALUES (?,?,?,?)",
                    (content, location, last_highlight_id, book_id)
                    )

if __name__ == '__main__':
    # FOR TESTING
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()
    for filename in os.listdir(test_dir_path):
        filepath = os.path.join(test_dir_path, filename)
        from_emailed_csv(cur, filepath)

    conn.commit()
    conn.close()