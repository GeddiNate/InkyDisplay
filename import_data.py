import sqlite3
import csv

note_sep = '=========='

def from_my_clippings_(conn, filename):
    with open(filename, encoding='utf-8-sig') as file:
        items = file.read().split(note_sep)
        data = [item.split('\n') for item in items if item != '']
        print(data)

def from_emailed_csv(conn, filename):
    with open(filename, encoding='utf-8') as file:
        reader = list(csv.reader(file))
        title = reader[1][0]
        author = reader[2][0]
        print(title)
        print(author)
        for row in reader:
            print(row)

#from_kindle_clippings_file('tmp', 'My Clippings.txt')
from_emailed_csv('tmp', 'Oathbringer_ Book Three of the Stormlight Archive-Notebook.csv')

