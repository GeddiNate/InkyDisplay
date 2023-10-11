from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
import highlight
import random

WIDTH = 800
HEIGHT = 480
H_MARGIN = 30
V_MARGIN = 30
FONT_SIZE = 24
LINE_PADDING = 6
FONT_LOC = "resources//DejaVuSerif.ttf"
display = auto()

def displayhighlight(q, b):

    # Load the image and resize it to fit screen
    try:
        img = Image.open(f"resources//{b.title}.jpg")
    except:
        img = Image.open("resources//nightSkytest.png")
    img = img.resize((WIDTH, HEIGHT)) # TODO move elsewhere

    # Get the width and height of the image
    width, height = img.size

    # Create a new ImageDraw object
    draw = ImageDraw.Draw(img)

    # Define the font and size for the text
    textFont = ImageFont.truetype(FONT_LOC, FONT_SIZE)
    titleFont = ImageFont.truetype(FONT_LOC, round(FONT_SIZE*0.6))
    authorFont = ImageFont.truetype(FONT_LOC, round(FONT_SIZE*0.4))

    # display book title and author
    title, author = str(b).splitlines()

    length = max(titleFont.getlength(title), authorFont.getlength(author))
    authorHeight = titleFont.getbbox(author)[3]
    titleHeight = titleFont.getbbox(title)[3] + authorHeight

    draw.text((WIDTH - H_MARGIN - length, HEIGHT - V_MARGIN - titleHeight), title, font=titleFont, fill=(255, 255, 0))
    draw.text((WIDTH - H_MARGIN - length, HEIGHT - V_MARGIN - authorHeight), author, font=authorFont, fill=(255, 255, 0))

    # Wrap the text to fit on the image
    lines = []
    words = str(q).replace('\n',' ').split(" ")
    currentLine = words[0]
    # for each word in the highlight
    for word in words[1:]:
        # if the current line plus the next word is shorter than the image width minus the hoizontal padding
        if textFont.getlength(currentLine + " " + word) < width - (H_MARGIN * 2):
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
        lineWidth, lineHeight = textFont.getbbox(line)[2:]
        xText = H_MARGIN
        draw.text((xText, yText), line, font=textFont, fill=(255, 255, 255))
        yText += lineHeight

    # Save the image with the text
    #img.save("resources//imageOut.png")
    display.set_image(img)
    display.show()

