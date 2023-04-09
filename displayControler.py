from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
import quote
import random

WIDTH = 600 
HEIGHT = 448
H_MARGIN = 30
V_MARGIN = 30

def displayQuote(q, b):

    # Load the image and resize it to fit screen
    img = Image.open("testImage.jpg")
    img = img.resize((WIDTH, HEIGHT)) # TODO move elsewhere

    # Get the width and height of the image
    width, height = img.size

    # Create a new ImageDraw object
    draw = ImageDraw.Draw(img)

    # Define the font and size for the text
    font = ImageFont.truetype("DejaVuSerif.ttf", 24)

    # Wrap the text to fit on the image
    lines = []
    words = str(q).split(" ")
    currentLine = words[0]
    # for each word in the quote
    for word in words[1:]:
        # if the current line plus the next word is shorter than the image width minus the hoizontal padding
        if font.getlength(currentLine + " " + word) < width - (H_MARGIN * 2):
            # add word to current line
            currentLine += " " + word
        else:
            # end current line and start next line
            lines.append(currentLine)
            currentLine = word
    lines.append(currentLine)

    # Draw the text on the image
    #yText = height - (len(lines) * 30) # adjust the 30 value to set the line spacing
    yText = V_MARGIN
    # for each line
    for line in lines:
        # get witdth and hiehgt of line
        lineWidth, lineHeight = font.getbbox(line)[2:]
        xText = H_MARGIN
        draw.text((xText, yText), line, font=font, fill=(255, 255, 255))
        yText += lineHeight

    infolines = str(b).splitlines()
    for line in infolines:
        # get witdth and hiehgt of line
        lineWidth, lineHeight = font.getbbox(line)[2:]
        xText = lineWidth +
    # Save the image with the text
    img.save("imageOut.png")

displayQuote()