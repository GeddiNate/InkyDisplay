from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
from highlight import Highlight
import random

class DisplayControler:
    WIDTH = 800
    HEIGHT = 480
    H_MARGIN = 30
    V_MARGIN = 30
    FONT_SIZE = 24
    LINE_PADDING = 6
    FONT_LOC = "resources//DejaVuSerif.ttf"
    #TODO seperate displayhiglight into various class functions
    def __init__(self):
        self.display = auto()

    def displayHighlight(self):

        # Load the image and resize it to fit screen
        try:
            img = Image.open(f"resources//{highlight.book.title}.jpg")
        except:
            img = Image.open("resources//nightSkytest.png")
        img = img.resize((DisplayControler.WIDTH, DisplayControler.HEIGHT)) # TODO move elsewhere

        # Get the width and height of the image
        width, height = img.size

        # Create a new ImageDraw object
        draw = ImageDraw.Draw(img)

        # Define the font and size for the text
        textFont = ImageFont.truetype(DisplayControler.FONT_LOC, DisplayControler.FONT_SIZE)
        titleFont = ImageFont.truetype(DisplayControler.FONT_LOC, round(DisplayControler.FONT_SIZE*0.6))
        authorFont = ImageFont.truetype(DisplayControler.FONT_LOC, round(DisplayControler.FONT_SIZE*0.4))

        # display book title and author
        authors = ', '.join(highlight.book.authors)

        length = max(titleFont.getlength(highlight.book.title), authorFont.getlength(authors))
        authorHeight = titleFont.getbbox(authors)[3]
        titleHeight = titleFont.getbbox(highlight.book.title)[3] + authorHeight

        # draw highlight text
        draw.text(
            (DisplayControler.WIDTH - DisplayControler.H_MARGIN - length, 
            DisplayControler.HEIGHT - DisplayControler.V_MARGIN - titleHeight), 
            highlight.book.title, 
            font=titleFont, fill=(255, 255, 0)
            )
        # draw authors and book title
        draw.text(
            (DisplayControler.WIDTH - DisplayControler.H_MARGIN - length, 
            DisplayControler.HEIGHT - DisplayControler.V_MARGIN - authorHeight),
            authors, 
            font=authorFont, fill=(255, 255, 0)
            )

        # Wrap the text to fit on the image
        lines = []
        words = str(highlight.text).replace('\n',' ').split(' ')
        currentLine = words[0]
        # for each word in the highlight
        for word in words[1:]:
            # if the current line plus the next word is shorter than the image width minus the hoizontal padding
            if textFont.getlength(currentLine + " " + word) < width - (DisplayControler.H_MARGIN * 2):
                # add word to current line
                currentLine += " " + word
            else:
                # end current line and start next line
                lines.append(currentLine)
                currentLine = word
        lines.append(currentLine)

        # Draw the text on the image
        #yText = height - (len(lines) * 30) # adjust the 30 value to set the line spacing
        yText = DisplayControler.V_MARGIN
        # for each line
        for line in lines:
            # get witdth and hiehgt of line
            lineWidth, lineHeight = textFont.getbbox(line)[2:]
            xText = DisplayControler.H_MARGIN
            draw.text((xText, yText), line, font=textFont, fill=(255, 255, 255))
            yText += lineHeight

        # Save the image with the text
        #img.save("resources//imageOut.png")
        self.display.set_image(img)
        self.display.show()

