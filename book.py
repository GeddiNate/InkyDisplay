
# class for storing all highlights from a particular book
class Book:
    def __init__(self, title, authors, subtitle=None):
        """
        Constructor
        Args:
            title: The title of the book.
            authors: An array containing the author(s) of the book.
            subtitle: The subtitle of the book.
            
        """
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.highlights = []
    
    def __str__(self):
        """
        Returns a string representation of the Book object for display.
        """
        return f"{self.title} \nBy: {self.authors}" #TODO list to str in visually appealing way
    

    def toJSON(self):
        """
        Converts the Book object to a dictionary for serialization.
        return: 
            A dictionary representation of the Book object.
        """
        retval = {'title': self.title}
        retval['authors'] = [author for author in self.authors]
        retval['highlights'] = [highlight.toJSON() for highlight in self.highlights]
        return retval
    
    def addHighlight(self, highlight):
        """
        Add a highlight to the Book.
        args:
            highlight: The highlight object to be added to this Book.
        """
        self.highlights.append(highlight)
