from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
import quote
import random

# get a random quote form the list of books 
# @params data list of book objects
def randomQuote(data):
    book = random.choice(data) # random book
    return random.choice(book.quotes) # random quote from book

def displayQuote():
    from PIL import Image, ImageDraw, ImageFont

    # Load the image
    img = Image.open("testImage.jpg")

    # Get the width and height of the image
    width, height = img.size

    # Create a new ImageDraw object
    draw = ImageDraw.Draw(img)

    # Define the font and size for the text
    font = ImageFont.truetype("arial.ttf", 24)

    # Define the text to display
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor."

    # Wrap the text to fit on the image
    lines = []
    words = text.split(" ")
    current_line = words[0]
    for word in words[1:]:
        if font.getsize(current_line + " " + word)[0] < width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    # Draw the text on the image
    y_text = height - (len(lines) * 30) # adjust the 30 value to set the line spacing
    for line in lines:
        line_width, line_height = font.getsize(line)
        x_text = (width - line_width) / 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
        y_text += line_height

    # Save the image with the text
    img.save("example_with_text.jpg")

displayQuote()