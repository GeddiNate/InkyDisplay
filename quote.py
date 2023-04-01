import json
import datetime
import random

# class for storing highlights as quotes
class Quote:
    
    def __init__(self, text, color, note) -> None:
        """Constructor

        :param string text: contains the text of the quote itself
        :param string color: contains the color of higlight used
        :param string note: contains any notes associtated with the text
        """
        self.text = text
        self.color = color
        self.note = note
    
    def __str__(self):
        if self.note == "":
            return self.text
        return f"{self.text} - {self.note}"

    def toJSON(self):
        """convert Quote to dict for serialization

        :return dictrionary: dict representation of Quote object
        """
        return {'text': self.text, 'color': self.color, 'note': self.note}


# class for storing all quotes from a particular book
# TODO support of multiple authors
class Book:
    def __init__(self, title, author, lastAccessed) -> None:
        """Constructor

        :param string title: contains the title of the book
        :param string author: contains the author of the book
        :param date lastAccessed: the date the book was last accessed on kindle
        """
        self.title = title
        self.author = author
        self.lastAccessed = lastAccessed
        self.quotes = []
    
    def __str__(self):
        return f"{self.title} \n By: {self.author}"
    

    def toJSON(self):
        """convert Book to dict for serialization

        :return dictionary: dict representation of Book object
        """
        retval = {'title': self.title, 'author':self.author, 'lastAccessed': datetime.date.isoformat(self.lastAccessed)}
        q = [] 
        for quote in self.quotes:
            q.append(quote.toJSON())
        retval['quotes'] = q
        return retval
    
    def addQuote(self, q):
        """Add a quote to the book

        :param Quote q: Quote object to be appended to self.quotes
        """
        self.quotes.append(q)


# class to contain a collection of books and helper methods 
# @books(list[Book]) contains a list of Book objects with all books synced to device
# TODO add metadata to this class a lastSynced var could replace lastAccessed
class BookList:
    def __init__(self):
        """Constructor
        """
        self.books = []
    
    # search data for book with matching title
    # @bookTitle title of book to search for
    # @return the book object if it is found, None if not found 
    def findBook(self, bookTitle):
        """Seach this BookList for a book with matching title

        :param string bookTitle: The title of the book to find
        :return Book: The Book object whose title matches the input param or None if not found
        """
        for book in self.books:
            if book.title == bookTitle:
                return book
        # if not found      
        return None
    
    def addBook(self, b):
        """Add a Book object to this BookList

        :param Book b: Book to be added to this BookList object
        """
        self.books.append(b)
    
    def removeBook(self, b):
        """Remove a Book object from this Booklist 

        :param Book b: Book object to be removed from BookList
        """
        self.books.remove(b)

    
    def randomQuote(self):
        """Get a random quote from all the quotes in all the books in this list

        :return tuple (Quote, Book): a tuple containing the randomly selected quote object and the book the quote came from
        """

        # Create a list of weights for each book, where the weight is the number of quotes
        weights = [len(book.quotes) for book in self.books]
        
        # Use the weights to get the index a random book
        b = random.choices(range(len(self.books)), weights=weights)[0]
        
        # Select a random quote from the selected book
        q = random.choice(self.books[b].quotes)
        
        return (q, self.books[b])
        

        """
        Selects a random value from a jagged array and returns the index of the nested array it came from.
        
        Args:
            jagged_array (list): A jagged array containing one or more nested arrays of varying lengths.
            
        Returns:
            A tuple containing the randomly selected value and the index of the nested array it came from.
        """
        # flat_array = [element for sublist in jagged_array for element in sublist]
        # index = random.randrange(len(jagged_array))
        # subarray_length = len(jagged_array[index])
        # random_index = random.randrange(subarray_length)
        # return (flat_array[random_index], index)



    def toJSON(self):
        """convert BookList to dict for serialization

        :return dictionary: dict representation of BookList object
        """
        retval = {}
        b = [] 
        for book in self.books:
            b.append(book.toJSON())
        retval['books'] = b
        return retval

# load stored quotes from json file
# @f an open file to read from 
# @return BookList conating all books and quotes that were found in file f
def loadQuotes(f):
    
    # open file and load data
    retval = BookList()
    data = json.load(f)
        
    # for each book in file create book object
    for item in data["books"]:
        b = Book(item['title'], item['author'], datetime.date.fromisoformat(item['lastAccessed']))
           
        # for each quote in book create a quote object
        for q in item['quotes']:
            b.addQuote(Quote(q['text'], q['color'], q['note']))
            
        retval.addBook(b)

    return retval


#test code

# q1 = Quote('text here', 239, 'yellow', 'heading', 'me')
# q2 = Quote('text here again', 560, 'purple', 'heading2', 'myself')

# b = Book("the book", 'some idiot')
# b.addQuote(q1)
# b.addQuote(q2)

# print(b.toJSON())

# print(json.dumps(b.toJSON()))


# test code for loadQuotes

# r = loadQuotes('output.json')
# print(r)
# print(type(r))
# print(len(r))
# for i in r:
#     print ('===============')
#     print(type(i))
#     for j in i.quotes:
#         print(type(j))
