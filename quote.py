import json

# class for storeing highlights as quotes
class Quote:
    def __init__(self, text, page, color, heading, speaker = "") -> None:
        self.text = text
        self.page = page
        self.color = color
        self.heading = heading
        self.speaker = speaker

    # convert to dict for serialization
    def toJSON(self):
        return {'text': self.text, 'page': self.page, 'color': self.color, 'heading': self.heading, 'speaker': self.speaker}


# class for storing all quotes from a particular book
class Book:
    def __init__(self, title, author) -> None:
        self.title = title
        self.author = author
        self.quotes = []

    # convert to dict for serialization
    def toJSON(self):
        retval = {'title': self.title, 'author':self.author, 'quotes':self.quotes}
        q = [] 
        for quote in self.quotes:
            q.append(quote.toJSON())
        retval['quotes'] = q
        return retval
    

#test code

# q1 = Quote('text here', 239, 'yellow', 'heading', 'me')
# q2 = Quote('text here again', 560, 'purple', 'heading2', 'myself')

# b = Book("the book", 'some idiot')
# b.addQuote(q1)
# b.addQuote(q2)

# print(b.toJSON())

# print(json.dumps(b.toJSON()))
