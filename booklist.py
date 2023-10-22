from datetime import date
import random
import json
import logging
from book import Book
from highlight import Highlight


# class to contain a collection of books and methods to interact with them
class BookList:

    # Filename where data should be stored and read from
    # TODO if there are multipule BookList's this may break
    FILE_NAME = 'book_highlight_data.json'

    # TODO is file_path needed
    def __init__(self, file_path = ""):
        """
        Constructor
        args:
            file_path: Path to where the highlight data is stored, defaults to the current dirctory .
        """
        self.file_path = file_path
        self.books = []
        # set last synced to min data so all data will be synced if no data is loaded
        self.last_successful_sync = date.min
    
    def findBook(self, book_title: str):
        """
        Seach this BookList for a book with a title that matches the argument.
        args:
            book_title The title of the book to find.
        return:
            The Book object with matching title or None if no book is found.
        """
        for book in self.books:
            if book.title == book_title:
                return book
            
        return None
    
    def addBook(self, book):
        """
        Append a Book object to this BookList object.
        """
        self.books.append(book)
    
    def removeBook(self, b):
        """
        Remove a Book object from this Booklist.
        """
        # TODO if fail
        self.books.remove(b)

    def randomHighlight(self):
        """
        Get a random Highlight from all the Highlights in all the Books in this BookList.
        return:
            The randomly selected Highlight object.
        """
        # Create a list of weights for each book, where the weight is the number of highlights
        weights = [len(book.highlights) for book in self.books]

        # Use the weights to get the index a random book
        book_index = random.choices(range(len(self.books)), weights=weights)[0]

        # Select a random highlight from the selected book
        highlight = random.choice(self.books[book_index].highlights)
        
        return highlight

    def save(self):
        """
        Serialize this BookList object to JSON and write it to a file.
        """
        with open(self.file_path + self.FILE_NAME, "w") as json_file:
            json_file.write(json.dumps(self.toJSON()))

    def load(self):
        """
        Attempt to load a BookList object from JSON file.
        """
        try:
            # open file and load data
            with open(self.file_path + self.FILE_NAME) as json_file:
                data = json.load(json_file)
                self.last_successful_sync = date.fromisoformat(data["last_successful_sync"])
                # for each book in file create book object
                for item in data["books"]:
                    b = Book(item['title'], item['author'])
                    # for each highlight in book create a highlight object
                    for h in item['highlights']:
                        b.addHighlight(Highlight(h['text'], b, h['color'], h['note']))
                    self.addBook(b)
        except Exception as e:
            logging.exception(e)

    def toJSON(self):
        """
        Convert BookList to a dictionary for serialization.

        :return 
            A dictionary representation of this BookList object.
        """
        retval = {'last_successful_sync': self.last_successful_sync.isoformat()}
        retval['books'] = [book.toJSON() for book in self.books]
        return retval