import json
import datetime

# class for storing highlights as quotes
class Quote:
    def __init__(self, text, color, note) -> None:
        self.text = text
        self.color = color
        self.note = note

    # convert to dict for serialization
    def toJSON(self):
        return {'text': self.text, 'color': self.color, 'note': self.note}


# class for storing all quotes from a particular book
class Book:
    def __init__(self, title, author, lastAccessed) -> None:
        self.title = title
        self.author = author
        self.lastAccessed = lastAccessed
        self.quotes = []

    # convert to dict for serialization
    def toJSON(self):
        retval = {'title': self.title, 'author':self.author, 'quotes':self.quotes}
        q = [] 
        for quote in self.quotes:
            q.append(quote.toJSON())
        retval['quotes'] = q
        return retval

# load stored quotes from json file
def loadQuotes(filename):
    
    # open file and load data
    retval = []
    with open(filename) as f:
        data = json.load(f)
        
        # for each book in file create book object
        for item in data:
            b = Book(item['title'], item['author'])
            
            # for each quote in book create a quote object
            for q in item['quotes']:
                b.quotes.append(Quote(q['text'], q['color'], q['note']))
            
            retval.append(b)

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