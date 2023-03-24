from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
import quote
import random

# get a random quote form the list of books 
# @params data list of book objects
def randomQuote(data):
    book = random.choice(data) # random book
    return random.choice(book.quotes) # random quote from book

def displayQuote(quote):
    img = Image.open('testImage.jpg')
    
    out = Image.new("RGB", (150, 100), (255, 255, 255))
    
    d = ImageDraw.Draw(out)

    # # get a font
    # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)

    # # draw multiline text
    d.multiline_text((10, 10), quote.text, fill=(0, 0, 0))

    # out.show()
    out.save("imageOut.png", 'PNG')


# load kindle highlight data
data = quote.loadQuotes('output.json')


with Image.open("testImage.jpg") as im:
    print(im.format, im.size, im.mode)
    im.show()
    

    # inky Example:
    # automatically get display info from EEPROM 
    # display = auto()


    # print(display.colour)
    # print(display.resolution)

    # display.set_image(im)

    # display.show()





    # # Example: Draw Partial Opacity Text

    # # make a blank image for the text, initialized to transparent text color
    # txt = Image.new("RGBA", im.size, (255, 255, 255, 0))

    # # get a font
    # #fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    # # get a drawing context
    # d = ImageDraw.Draw(txt)

    # # draw text, half opacity
    # #d.text((10, 10), "Hello", font=fnt, fill=(255, 255, 255, 128))
    # d.text((10, 10), "Hello", fill=(0, 0, 0, 128))
    # # draw text, full opacity
    # #d.text((10, 60), "World", font=fnt, fill=(255, 255, 255, 255))
    # d.text((10, 60), "World", fill=(0, 0, 0, 255))
    # im = im.convert("RGBA")
    # print(im, txt)
    # out = Image.alpha_composite(im, txt)



