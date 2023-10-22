from book import Book

class Highlight:

    def __init__(self, text: str, book: Book, color: str, note: str=None) -> None:
        """
        Constructor
        args:
            text: The text of the highlight.
            book: The Book object that represents the book this highlight is from.
            color: The color used to higlight highlight the text.
            note: Contains any notes associtated with the highlighted text.
        """
        self.text = text
        self.book = book
        self.color = color
        self.note = note
    
    def __str__(self) -> str:
        """
        Returns string representation of Highlight object for display.
        """
        if self.note == None:
            return self.text
        return f"{self.text} - {self.note}"

    def toJSON(self):
        """
        Convert Highlight to dictionary for serialization.
        :return 
            Dictrionary representation of the Highlight object.
        """
        return {
            'text': self.text, 
            'book': self.book, 
            'color': self.color, 
            'note': self.note}