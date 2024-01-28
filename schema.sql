DROP TABLE IF EXISTS highlights;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS artwork;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS book_art;

-- Table to store individual highlights
CREATE TABLE highlights (
    highlight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    color TEXT DEFAULT NUll,
    location_start INTEGER DEFAULT NULL,
    location_end INTEGER DEFAULT NULL,
    page INTEGER DEFAULT NULL,
    showable INTEGER NOT NULL DEFAULT TRUE,
    shown INTEGER NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    book_id INTEGER DEFAULT NULL,
    UNIQUE(content, book_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Table to store notes from kindle
CREATE TABLE notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT NOT NULL,
    location_start INTEGER DEFAULT NULL,
    location_end INTEGER DEFAULT NULL,
    page INTEGER DEFAULT NULL,
    highlight_id INTEGER DEFAULT NULL,
    book_id INTEGER DEFAULT NULL,
    FOREIGN KEY (highlight_id) REFERENCES highlights(highlight_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    UNIQUE(note, location_start, location_end, page, highlight_id, book_id)
);

-- Table to store information about books
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255) DEFAULT NULL,
    UNIQUE (title, subtitle)
);

-- Table to store information about authors
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    UNIQUE (name)
);

-- Table to store filepaths for artwork
CREATE TABLE artwork (
    art_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT DEFAULT NULL,
    filepath TEXT NOT NULL

);

-- Junction table linking books and authors
CREATE TABLE book_authors (
    book_id INTEGER,
    author_id INTEGER,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Junction table linking books and artwork
CREATE TABLE book_art (
    book_id INTEGER,
    art_id INTEGER,
    PRIMARY KEY (book_id, art_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (art_id) REFERENCES artwork(art_id)
);



