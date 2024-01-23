from book import Book

class Highlight:

    def __init__(self, text, book, visible=True, note=None):
        """
        Constructor
        args:
            text: The text of the highlight.
            book: The Book object that represents the book this highlight is from.
            visible: The color used to higlight highlight the text.
            note: Contains any notes associtated with the highlighted text.
        """
        self.text = text
        self.book = book
        self.visible = visible
        self.note = note
    
    def __str__(self):
        """
        Returns string representation of Highlight object for display.
        """
        if self.note == None:
            return self.text
        return f"{self.text} - {self.note}"

    def toDict(self):
        """
        Return a Dictrionary representation of this object .
        """
        return {
            'text': self.text, 
            'color': self.color, 
            'note': self.note
            }