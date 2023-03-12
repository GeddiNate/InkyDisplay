import jsonpickle

class Quote:
    def __init__(self, text, page, color, heading, speaker = "") -> None:
        self.text = text
        self.page = page
        self.color = color
        self.heading = heading
        self.speaker = speaker

class Book:
    def __init__(self, title, author) -> None:
        self.title = title
        self.author = author
        self.quotes = []
    
    def addQuote(self, quote):
        self.quotes.append(quote)

def quote_encoder(quote):
    if isinstance(quote, Quote):
        return {'text': quote.text, 'page': quote.page, 'color': quote.color, 'heading': quote.heading, 'speaker': quote.speaker}
    
    raise TypeError(f'Object {quote} is not of type Quote')

def book_encoder(book):
    if isinstance(book, Book):
        return {'title': book.title, 'author':book.author, 'quotes':book.quotes}
    
    raise TypeError(f'Object {book} is not of type Book')
    

#test code

# q1 = Quote('text here', 239, 'yellow', 'heading', 'me')
# q2 = Quote('text here again', 560, 'purple', 'heading2', 'myself')

# b = Book("the book", 'some idiot')
# b.addQuote(q1)
# b.addQuote(q2)

# print(jsonpickle.encode(q1))
# print(jsonpickle.encode(q2))
# print(jsonpickle.encode(b))        