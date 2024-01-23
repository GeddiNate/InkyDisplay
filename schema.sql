DROP TABLE IF EXISTS highlights;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS artwork;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS book_art;

-- Table to store individual highlights
CREATE TABLE highlights (
    highlight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    visible INT NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    note TEXT DEFAULT NULL,
    book_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Table to store information about books
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subtitle TEXT NOT NULL
);

-- Table to store information about authors
CREATE TABLE authors (
    author_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table to store filepaths for artwork
CREATE TABLE artwork (
    art_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT DEFAULT NULL,
    filepath TEXT NOT NULL

);

-- Junction table linking books and authors
CREATE TABLE book_authors (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Junction table linking books and artwork
CREATE TABLE book_art (
    book_id INT,
    art_id INT,
    PRIMARY KEY (book_id, art_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (art_id) REFERENCES artwork(art_id)

);



