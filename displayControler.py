from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont


with Image.open("testImage.jpg") as im:
    print(im.format, im.size, im.mode)
    im.show()
    
    # automatically get display info from EEPROM 
    # display = auto()


    # print(display.colour)
    # print(display.resolution)

    # display.set_image(im)

    # display.show()


    # Example: Draw a gray cross over an image

    # draw = ImageDraw.Draw(im)
    # draw.line((0, 0) + im.size, fill=128)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)


    # Example: Draw Partial Opacity Text

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", im.size, (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10, 10), "Hello", font=fnt, fill=(255, 255, 255, 128))
    # draw text, full opacity
    d.text((10, 60), "World", font=fnt, fill=(255, 255, 255, 255))

    out = Image.alpha_composite(im, txt)

    




    # Example: Draw Multiline Text

    # from PIL import Image, ImageDraw, ImageFont

    # # create an image
    # out = Image.new("RGB", (150, 100), (255, 255, 255))

    # # get a font
    # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    # # get a drawing context
    # d = ImageDraw.Draw(out)

    # # draw multiline text
    # d.multiline_text((10, 10), "Hello\nWorld", font=fnt, fill=(0, 0, 0))

    # out.show()

    out.save("imageOut.png", 'PNG')
    #im.save("imageOut.png", 'PNG')
